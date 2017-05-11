from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
import json
from .models import Session, Program, Enroll, Student
from django.db.models import F

# Create your views here.


def index(request):
    context = {'user': request.user}
    return render(request, 'students/index.html', context)  



@api_view(['GET'])
def get_filter_options(request):
    filter_options = []

    sessions = Session.objects.all().annotate(val=F('session')).values("val")
    #sessions = Enroll.objects.all().annotate(val=F('session')).values("val").distinct()
    enrolled_session = {"field": "enrolled_sessions", "title": "Session Enrolled", "options": sessions}

    program_types = Program.objects.all().annotate(val=F('program_type')).values("val").distinct()
    enroll_program_types = {"field": "enroll_program_type", "title": "Program Type", "options": program_types}

    program_level = Program.objects.all().annotate(val=F('level')).values("val").distinct()
    enroll_program_levels = {"field": "enroll_program_level", "title": "Program Level", "options": program_level}

    programs = Program.objects.all().annotate(val=F('program'), hover=F('name')).values("val", "hover")
    #programs = Enroll.objects.all().annotate(val=F('program')).values("val").distinct()
    enrolled_program = {"field": "enrolled_programs", "title": "Program Enrolled", "options": programs}


    filter_options.append(enrolled_session)
    filter_options.append(enroll_program_types)
    filter_options.append(enroll_program_levels)
    filter_options.append(enrolled_program)
    return Response(filter_options)

@api_view(['GET'])
def filter_enroll_program_type(request):
    programs = Program.objects.all()

    f_type = request.query_params['type'].split(',')
    if f_type[0] != '':
        programs = programs.filter(program_type__in=f_type)

    f_level = request.query_params['level'].split(',')
    if f_level[0] != '':
        programs = programs.filter(level__in=f_level)

    programs = programs.annotate(val=F('program'), hover=F('name')).values("val", "hover")
    return Response(programs)



@api_view(['POST'])
def filter_students(request):
    filters = json.loads(request.data['filters'])
    students = Student.objects.all()

    if 'enrolled_sessions' in filters:
        students = students.filter(enroll__session__in=filters['enrolled_sessions']).distinct()

    if 'enroll_program_type' in filters:
        students = students.filter(enroll__program__program_type__in=filters['enroll_program_type']).distinct()

    if 'enroll_program_level' in filters:
        students = students.filter(enroll__program__level__in=filters['enroll_program_level']).distinct()

    if 'enrolled_programs' in filters:
        students = students.filter(enroll__program__in=filters['enrolled_programs']).distinct()

    response = {"count": students.count(), "students": students.values('given_name', 'student_number')}


    return Response(response)