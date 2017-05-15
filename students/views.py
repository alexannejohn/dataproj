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

    ###
    #  Options for filtering by student details
    ###
    student_options = []

    provinces_raw = Student._meta.get_field('province').choices
    provinces = [{"val": a[0], "hover": a[1]} for a in provinces_raw]
    student_provinces = {"field": "student_province", "title": "Province", "options": provinces}

    student_options.append(student_provinces)


    ###
    #  Options for filtering by enrollment
    ###
    enroll_options = []

    sessions = Session.objects.all().order_by("year", "code").annotate(val=F('session')).values("val")
    #sessions = Enroll.objects.all().annotate(val=F('session')).values("val").distinct()
    enroll_sessions = {"field": "enroll_session", "title": "Session Enrolled", "options": sessions}

    program_types = Program.objects.all().order_by("program_type").annotate(val=F('program_type')).values("val").distinct()
    enroll_program_types = {"field": "enroll_program_type", "title": "Program Type", "options": program_types}

    program_levels = Program.objects.all().order_by("level").annotate(val=F('level')).values("val").distinct()
    enroll_program_levels = {"field": "enroll_program_level", "title": "Program Level", "options": program_levels}

    programs = Program.objects.all().order_by("program").annotate(val=F('program'), hover=F('name')).values("val", "hover")
    #programs = Enroll.objects.all().annotate(val=F('program')).values("val").distinct()
    enroll_programs = {"field": "enroll_program", "title": "Program Enrolled", "options": programs}


    enroll_options.append(enroll_sessions)
    enroll_options.append(enroll_program_types)
    enroll_options.append(enroll_program_levels)
    enroll_options.append(enroll_programs)


    return Response({"enroll_options": enroll_options, "student_options": student_options})

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

    ###
    #  filtering by student details
    ###

    if 'student_province' in filters:
        students = students.filter(province__in=filters['student_province'])

    ###
    #  filtering by enrollment
    ###

    if 'enroll_session' in filters:
        students = students.filter(enroll__session__in=filters['enroll_session']).distinct()

    if 'enroll_program_type' in filters:
        students = students.filter(enroll__program__program_type__in=filters['enroll_program_type']).distinct()

    if 'enroll_program_level' in filters:
        students = students.filter(enroll__program__level__in=filters['enroll_program_level']).distinct()

    if 'enroll_program' in filters:
        students = students.filter(enroll__program__in=filters['enroll_program']).distinct()


    ###
    #  return list of students
    ###
    response = {"count": students.count(), "students": students.values('given_name', 'student_number')}


    return Response(response)