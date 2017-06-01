from rest_framework import serializers
from .models import Student, Enroll, Application, Graduation, Award


class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = ('session', 'program', 'specialization_1', 'specialization_2')

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('session', 'program')

class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = ('program', 'ceremony_date')

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('session', 'award_title')

class StudentSerializer(serializers.ModelSerializer):
    most_recent_enrollment = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'most_recent_enrollment')


class StudentDetailSerializer(serializers.ModelSerializer):
    enrollments = EnrollSerializer(read_only=True, many=True)
    applications = ApplicationSerializer(read_only=True, many=True)
    graduations = GraduationSerializer(read_only=True, many=True)
    awards = AwardSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'enrollments', 'applications', 'graduations', 'awards', 'province')
