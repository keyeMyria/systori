from datetime import datetime, timedelta, date
from collections import OrderedDict

from django.db.models.query import QuerySet
from django.db.models import F, Sum, Min, Max
from django.utils import timezone
from django.contrib.auth import get_user_model


class TimerQuerySet(QuerySet):

    def get_duration(self):
        return self.aggregate(total_duration=Sum('duration'))['total_duration'] or 0

    def filter_running(self):
        return self.filter(end__isnull=True)

    def filter_today(self):
        return self.filter(start__gte=timezone.now().date())

    def filter_period(self, year=None, month=None):
        date_filter = {}
        assert not (month and not year), 'Cannot generate report by month without a year specified'
        if year:
            date_filter['start__year'] = year
            if month:
                date_filter['start__month'] = month
        else:
            now = timezone.now()
            date_filter['start__year'] = now.year
            date_filter['start__month'] = now.month
        return self.filter(**date_filter)

    def group_for_report(self):
        offset_seconds = timezone.get_current_timezone().utcoffset(datetime.now()).seconds
        return self.extra(
            select={'date': 'date(start + interval \'{} seconds\')'.format(offset_seconds)}
        ).values('kind', 'date', 'user_id').order_by().annotate(
            total_duration=Sum('duration'),
            day_start=Min('start'),
            latest_start=Max('start'),
            day_end=Max('end')
        ).order_by('-day_start')

    def generate_user_report_data(self):
        from calendar import monthrange
        from .utils import format_seconds

        now = timezone.now()
        queryset = self.filter_period(now.year, now.month).group_for_report().order_by('day_start')
        report = OrderedDict()
        for row in queryset:
            report_row = report.setdefault(row['date'], [])
            print(row)
            if row['kind'] == self.model.WORK:
                duration_calculator = self.model.duration_formulas[self.model.WORK]
                next_day = row['date'] + timedelta(days=1)
                total_duration = row['total_duration']
                # We have a running timer (possibly with existing stopped timers)
                if not row['day_end'] or row['latest_start'] > row['day_end']:
                    total_duration += duration_calculator(row['latest_start'], next_day)

                if row['total_duration'] >= self.model.DAILY_BREAK:
                    total = total_duration - self.model.DAILY_BREAK
                else:
                    total = total_duration

                overtime = total - self.model.WORK_HOURS if total > self.model.WORK_HOURS else 0
                report_row.append({
                    'kind': 'work',
                    'total_duration': total_duration,
                    'total': total,
                    'overtime': overtime,
                    'day_start': row['day_start'],
                    'day_end': row['day_end']
                })
            elif row['kind'] == self.model.HOLIDAY:
                report_row.append({
                    'kind': 'holiday',
                    'day_start': row['day_start'],
                    'total_duration': row['total_duration']
                })
            elif row['kind'] == self.model.ILLNESS:
                report_row.append({
                    'kind': 'illness',
                    'day_start': row['day_start'],
                    'total_duration': row['total_duration']
                })
        return report

    def generate_report_data(self):
        report_data = self.group_for_report()

        for day in report_data:
            real_day_end = day['date'] + timedelta(days=1)
            duration_calculator = self.model.duration_formulas[day['kind']]

            # if not day['day_end'] and day['day_start']:
            #     day['total_duration'] += duration_calculator(day['day_start'], timezone.now())

            # We have a running timer (possibly with existing stopped timers)
            if not day['day_end'] or day['latest_start'] > day['day_end']:
                day['total_duration'] += duration_calculator(day['latest_start'], real_day_end)

            if day['total_duration'] >= self.model.DAILY_BREAK:
                total = day['total_duration'] - self.model.DAILY_BREAK
            else:
                total = day['total_duration']
            overtime = total - self.model.WORK_HOURS if total > self.model.WORK_HOURS else 0
            day.update({
                'total': total,
                'overtime': overtime
            })
            yield day
