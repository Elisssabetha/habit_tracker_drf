import datetime

from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):

        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError('Нельзя одновременно указывать и связанную привычку и вознаграждение')

        if data.get('execution_time'):
            if data.get('execution_time') > datetime.time(hour=0, minute=2, second=0):
                raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд')

        if data.get('related_habit') and not data.get('related_habit').is_pleasant:
            raise serializers.ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной привычки')

        if data.get('is_pleasant') and (data.get('related_habit') or data.get('reward')):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')

        if data.get('frequency'):
            if data.get('frequency') > 7:
                raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

        return data
