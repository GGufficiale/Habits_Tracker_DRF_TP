from rest_framework import serializers


class HabitsValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value['is_good']:
            if value['related'] or value['prize']:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки или вознаграждения')
            if value['related'] and value['prize']:
                raise serializers.ValidationError(
                    'Может быть связанная привычка или вознаграждение,')
            if value['duration'] > 2:
                raise serializers.ValidationError(
                    'Длительность привычки не может быть больше 2 минут')
            if value['related']:
                if not value['related'].is_good:
                    raise serializers.ValidationError('Связанные привычки = приятные привычки')
