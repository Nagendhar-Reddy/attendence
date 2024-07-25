from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class WeeklyOffSerializer(serializers.ModelSerializer):
    day = serializers.ListField(
        child=serializers.ChoiceField(choices=WeeklyOff.DAY_CHOICES),
        write_only=True
    )

    class Meta:
        model = WeeklyOff
        fields = ['staff', 'day']

    def validate_day(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('The "day" field must be a list.')
        return value

    def create(self, validated_data):
        staff = validated_data['staff']
        days = validated_data['day']
        weekly_offs = [WeeklyOff(staff=staff, day=day) for day in days]
        WeeklyOff.objects.bulk_create(weekly_offs)
        return validated_data

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'





class ShiftChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftChangeRequest
        fields = '__all__'
    
    def create(self, validated_data):
        return ShiftChangeRequest.objects.create(**validated_data)