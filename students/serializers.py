from rest_framework import serializers
from .models import Student

# Serializers define the API representation.
class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('student_number', 'given_name')