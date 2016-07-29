from rest_framework import serializers

from .models import Timer
from . import utils


class TimerStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = ('start_latitude', 'start_longitude')

    def create(self, validated_data):
        return Timer.launch(user=self.context['user'], **validated_data)


class TimerStopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = ('end_latitude', 'end_longitude')


class TimerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = ('kind', 'date', 'start', 'end', 'duration')

    kind = serializers.CharField(source='get_kind_display')
    date = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    def get_date(self, obj):
        return utils.to_current_timezone(obj.start).strftime('%d.%m.%Y')

    def get_start(self, obj):
        return utils.to_current_timezone(obj.start).strftime('%H:%M')

    def get_end(self, obj):
        return utils.to_current_timezone(obj.end).strftime('%H:%M') if obj.end else '—'

    def get_duration(self, obj):
        return utils.format_seconds(obj.duration) if obj.duration else '—'