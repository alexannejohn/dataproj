from rest_framework import serializers
from .models import Student, Enroll

# Serializers define the API representation.
class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = ('session', 'program')


class StudentSerializer(serializers.ModelSerializer):
    enrollments = EnrollSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'enrollments')
