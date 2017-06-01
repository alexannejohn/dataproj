from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
import json
from .models import Session, Enroll, Student, Application, Graduation, Award
from studyareas.models import Subject, Specialization, Program
from codetables.models import RegistrationStatus, SessionalStanding
from django.db.models import F
from django.db.models import Q
from .serializers import StudentSerializer, StudentDetailSerializer
from django.http import HttpResponse, JsonResponse
import csv
from urllib.parse import urlparse, parse_qs
# Create your views here.


def index(request):
    context = {'user': request.user}
    return render(request, 'students/index.html', context)  


#
# This api view loads all the possible options for filtering students, ie each set of checkbox values
#
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

    sessions = Session.objects.all().order_by("year", "code").reverse().annotate(val=F('session')).values("val")
    #sessions = Enroll.objects.all().annotate(val=F('session')).values("val").distinct()
    enroll_sessions = {"field": "enroll_session", "title": "Session Enrolled", "options": sessions}

    year_levels = Enroll.objects.all().order_by("year_level").annotate(val=F("year_level")).values("val").distinct()
    enroll_year_levels = {"field": "enroll_year_level", "title": "Year Level", "options": year_levels}

    ee = Enroll.objects.all().values('regi_status').distinct()
    regi_statii = RegistrationStatus.objects.filter(status_code__in=ee).filter(hidden=False).annotate(val=F("status_code"), hover=F('description')).values("val", "hover")
    enroll_regi_statii = {"field": "enroll_regi_status", "title": "Registration Status", "options": regi_statii}

    es = Enroll.objects.all().values('sessional_standing').distinct()
    sessional_standings = SessionalStanding.objects.filter(standing_code__in=es).filter(hidden=False).annotate(val=F("standing_code"), hover=F('description')).values("val", "hover")
    enroll_sessional_standings = {"field": "enroll_sessional_standing", "title": "Sessional Standing", "options": sessional_standings}

    program_types = Program.objects.all().order_by("program_type").annotate(val=F('program_type')).values("val").distinct()
    enroll_program_types = {"field": "enroll_program_type", "title": "Program Type", "options": program_types}

    program_levels = Program.objects.all().order_by("level").annotate(val=F('level')).values("val").distinct()
    enroll_program_levels = {"field": "enroll_program_level", "title": "Program Level", "options": program_levels}

    programs = Program.objects.all().order_by("program").filter(hidden=False).annotate(val=F('program'), hover=F('name')).values("val", "hover")
    #programs = Enroll.objects.all().annotate(val=F('program')).values("val").distinct()
    enroll_programs = {"field": "enroll_program", "title": "Program Enrolled", "options": programs}

    subjects = Subject.objects.all().order_by('subject_code').filter(hidden=False).annotate(val=F('subject_code'), hover=F('name')).values("val", "hover")
    enroll_subjects = {"field": "enroll_subject", "title": "Specialization Subjects", "options": subjects}

    specializations = Specialization.objects.all().order_by('description').filter(hidden=False).annotate(text=F('description'), val=F('code'), hover=F('code')).values('val', 'text', 'hover')
    enroll_specializations = {"field": "enroll_specialization", "title": "Specializations", "options": specializations}


    enroll_options.append(enroll_sessions)
    enroll_options.append(enroll_year_levels)
    enroll_options.append(enroll_regi_statii)
    enroll_options.append(enroll_sessional_standings)
    enroll_options.append(enroll_program_types)
    enroll_options.append(enroll_program_levels)
    enroll_options.append(enroll_programs)
    enroll_options.append(enroll_subjects)
    enroll_options.append(enroll_specializations)


    application_options = []
    graduation_options = []
    award_options = []




    return Response(
        {"enroll_options": enroll_options, 
        "student_options": student_options, 
        "application_options": application_options,
        "graduation_options": graduation_options,
        "award_options": award_options}
        )


#
# Filters programs bases on program types and levels selected
#
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


#
# Filters specializations based on programs and subjects selected
#
@api_view(['GET'])
def filter_specialization(request):
    specializations = Specialization.objects.all()
    f_program = request.query_params['program'].split(',')
    if f_program[0] != '':
        specializations = specializations.filter(program__in=f_program)

    f_subj = request.query_params['subject'].split(',')
    if f_subj[0] != '':
        specializations = specializations.filter(Q(primary_subject__in=f_subj) | Q(secondary_subject__in=f_subj))

    specializations = specializations.annotate(text=F('description'), val=F('code'), hover=F('code')).values('val', 'text', 'hover')
    return Response(specializations)


#
# Takes json with all filter parameters as payload, returns list of students
#
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

    if 'enroll_year_level' in filters:
        students = students.filter(enroll__year_level__in=filters['enroll_year_level']).distinct()

    if 'enroll_regi_status' in filters:
        students = students.filter(enroll__regi_status__in=filters['enroll_regi_status']).distinct()

    if 'enroll_sessional_standing' in filters:
        students = students.filter(enroll__sessional_standing__in=filters['enroll_sessional_standing']).distinct()

    if 'enroll_program_type' in filters:
        students = students.filter(enroll__program__program_type__in=filters['enroll_program_type']).distinct()

    if 'enroll_program_level' in filters:
        students = students.filter(enroll__program__level__in=filters['enroll_program_level']).distinct()

    if 'enroll_program' in filters:
        students = students.filter(enroll__program__in=filters['enroll_program']).distinct()

    if 'enroll_subject' in filters:
        subj_specializations = Specialization.objects.filter(Q(primary_subject__in=filters['enroll_subject']) | Q(secondary_subject__in=filters['enroll_subject']))
        students = students.filter(enroll__specializations__in=subj_specializations).distinct()

    if 'enroll_specialization' in filters:
        specializations = Specialization.objects.filter(code__in=filters['enroll_specialization'])
        students = students.filter(enroll__specializations__in=specializations).distinct()


    ###
    #  search by student number
    ###
    if 'student_number' in filters:
        students = students.filter(student_number=filters['student_number'])

    ###
    #  return list of students
    ###
    # response = {"count": students.count(), "students": students.values('given_name', 'student_number')}

    serializer = StudentSerializer(students, many=True)
    numbers = ''.join(["student_number=" + str(x['student_number']) + "&" for x in serializer.data])
    return JsonResponse({"count": students.count(), "students": serializer.data, "numbers": numbers }, safe=False)


    # return Response(response)


@api_view(['GET'])
def student_detail(request):
    params = parse_qs(request.META['QUERY_STRING'])
    student_number = params['student_number'][0]
    student = Student.objects.get(student_number=student_number)
    serializer = StudentDetailSerializer(student)
    return JsonResponse({"student_details": serializer.data})

#
# Query url contains each student_number to be included in CSV. builds and returns CSV file
#
def csv_view(request):
    params = parse_qs(request.META['QUERY_STRING'])
    print(params['student_number'])
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['student_number', 'name', 'session', 'program_enrolled', 'application_program', 'awards', 'award_total'])
    for student_number in params['student_number']:
        student = Student.objects.get(student_number=student_number)
        sessions_e = Enroll.objects.filter(student_number=student_number).values('session').distinct()
        sessions_e = [x['session'] for x in sessions_e]
        sessions_a = Application.objects.filter(student_number=student_number).values('session').distinct()
        sessions_a = [x['session'] for x in sessions_a]
        sessions_aw = Award.objects.filter(student_number=student_number).values('session').distinct()
        sessions_aw = [x['session'] for x in sessions_aw]
        sessions = list(set().union(sessions_a, sessions_e, sessions_aw))
        if len(sessions) > 0:
            sessions.sort()
        for index, session in enumerate(sessions):
            programs = Enroll.objects.filter(student_number=student_number, session=session).values('program')
            if len(programs) > 0:
                program = programs[0]
            else:
                program = {'program': ""}

            applications = Application.objects.filter(student_number=student_number, session=session).values('program')
            if len(applications) > 0:
                app = applications[0]
            else:
                app = {"program": ""}

            awards = Award.objects.filter(student_number=student_number, session=session).values('award_title', 'award_amount')
            if len(awards) > 0:
                titles = (',').join([x['award_title'] for x in awards])
                total = sum(x['award_amount'] for x in awards)
                aw = {"titles": titles, "total": total}
            else:
                aw = {"titles": "", "total": 0}


            if index == 0:
                row = [student_number, student.given_name, session, program['program'], app['program'], aw['titles'], aw['total']]
            else:
                row = ["", "", session, program['program'], app['program'], aw['titles'], aw['total']]
            writer.writerow(row) 


    return response
    # return JsonResponse({"test": "test"})