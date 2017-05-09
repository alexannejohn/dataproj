from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer



# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer