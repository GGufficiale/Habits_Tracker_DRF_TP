from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabitsValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'
        validators = [HabitsValidator]
