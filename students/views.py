from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
import json
from .models import Session, Program, Enroll, Student
from django.db.models import F

# Create your views here.


def index(request):
    context = {'test': 'test'}
    return render(request, 'students/index.html', context)  



@api_view(['GET'])
def get_filter_options(request):
    filter_options = []

    # Filter 1: filter by session enrolled in
    sessions = Enroll.objects.all().annotate(val=F('session')).values("val").distinct()
    enrolled_session = {"field": "enrolled_sessions", "title": "Session Enrolled", "options": sessions}

    # Filter 2: filter by program enrolled in
    programs = Enroll.objects.all().annotate(val=F('program')).values("val").distinct()
    enrolled_program = {"field": "enrolled_programs", "title": "Program Enrolled", "options": programs}







    filter_options.append(enrolled_session)
    filter_options.append(enrolled_program)
    return Response(filter_options)



@api_view(['POST'])
def filter_students(request):
    filters = json.loads(request.data['filters'])
    students = Student.objects.all()

    # Filter 1: filter by session enrolled in
    students = students.filter(enroll__session__in=filters['enrolled_sessions']).distinct()

    # Filter 2: filter by program enrolled in
    students = students.filter(enroll__program__in=filters['enrolled_programs']).distinct()


    return Response(students.values('given_name'))