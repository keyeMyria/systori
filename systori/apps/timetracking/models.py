import json

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext as __

from .managers import TimerQuerySet


class Timer(models.Model):
    WORK = 10
    HOLIDAY = 20
    ILLNESS = 30
    KIND_CHOICES = (
        (WORK, _('Work')),
        (HOLIDAY, _('Holiday')),
        (ILLNESS, _('Illness'))
    )
    DAILY_BREAK = 60 * 60  # minutes

    duration_formulas = {
        WORK: lambda start, end: (end - start).total_seconds(),
        HOLIDAY: lambda start, end: -(end - start).total_seconds()
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    start = models.DateTimeField(auto_now_add=True, db_index=True)
    end = models.DateTimeField(blank=True, null=True, db_index=True)
    duration = models.IntegerField(default=0, help_text=_('in seconds'))
    kind = models.PositiveIntegerField(default=WORK, choices=KIND_CHOICES, db_index=True)

    objects = TimerQuerySet.as_manager()

    class Meta:
        verbose_name = _('timer')
        verbose_name_plural = _('timers')
        ordering = ('start',)

    @classmethod
    def launch(cls, user):
        """
        Convenience method for consistency (so the class has not just stop but launch method as well)
        """
        timer = cls(user=user)
        timer.save()
        return timer

    @property
    def is_running(self):
        return not self.end

    def save(self, *args, **kwargs):
        if not self.pk and type(self).objects.filter(user=self.user, end__isnull=True).exists():
            raise ValidationError(_('Timer already running'))
        super().save(*args, **kwargs)

    def get_duration_seconds(self, now=None):
        if self.duration:
            return self.duration
        if not now:
            now = timezone.now()
        return self.duration_formulas[self.kind](self.start, now)

    def get_duration(self, now=None):
        seconds = self.get_duration_seconds(now)
        return [int(v) for v in (seconds // 3600, (seconds % 3600) // 60, seconds % 60)]

    def stop(self):
        assert self.pk
        self.end = timezone.now()
        self.duration = self.get_duration_seconds(self.end)
        self.save()

    def to_json(self):
        return json.dumps({'duration': self.get_duration()})
