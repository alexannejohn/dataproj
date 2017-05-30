from rest_framework import serializers
from .models import Student, Enroll, Application, Graduation, Award

#enrollment details to be displayed in student table
class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = ('session', 'program', 'specialization_1', 'specialization_2')

#application details to be displayed in student table
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('session', 'program')

#graduation details to be displayed in student table
class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = ('program', 'ceremony_date')

#award details to be displayed in student table
class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('session', 'award_title')

# all student data
class StudentSerializer(serializers.ModelSerializer):
    enrollments = EnrollSerializer(read_only=True, many=True)
    applications = ApplicationSerializer(read_only=True, many=True)
    graduations = GraduationSerializer(read_only=True, many=True)
    awards = AwardSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'enrollments', 'applications', 'graduations', 'awards', 'province')
