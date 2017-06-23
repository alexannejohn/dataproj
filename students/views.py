from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import json
from .models import Session, Enroll, Student, Application, Graduation, Award
from studyareas.models import Subject, Specialization, Program
from codetables.models import RegistrationStatus, SessionalStanding, AppDecision, AppActionCode, AppStatus, AppReason, GradAppStatus
from codetables.models import AwardType
from django.db.models import F
from django.db.models import Q
from .serializers import StudentSerializer, StudentDetailSerializer
from django.http import HttpResponse, JsonResponse
import csv
from urllib.parse import parse_qs
from geojson import FeatureCollection, Point, Feature
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

    ids_raw = Student._meta.get_field('self_id').choices
    ids = [{"val": a[0], "text": a[1]} for a in ids_raw]
    student_ids = {"field": "student_self_id", "title": "Self ID", "options": ids}

    boolean_options = [{"val": "True", "text":"Yes"}, {"val": "False", "text":"No"}]

    student_band_fundings = {"field": "student_band_funding", "title": "Band Funding", "options": boolean_options}
    student_financial_holds = {"field": "student_financial_hold", "title": "Financial Hold", "options": boolean_options}

    student_options.append(student_provinces)
    student_options.append(student_ids)
    student_options.append(student_band_fundings)
    student_options.append(student_financial_holds)


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

    averages = [{"val": (0,50), "text": "<50"}, {"val": (50.1,70), "text": "50.1-70"}, {"val": (70.1,90), "text": "70.1-90"}]
    enroll_averages = {"field": "enroll_average", "title": "Sessional Average", "options": averages}

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
    enroll_options.append(enroll_averages)
    enroll_options.append(enroll_program_types)
    enroll_options.append(enroll_program_levels)
    enroll_options.append(enroll_programs)
    enroll_options.append(enroll_subjects)
    enroll_options.append(enroll_specializations)


    ###
    #  Options for filtering by application
    ###
    application_options = []

    application_sessions = {"field": "application_session", "title": "Session Applied", "options": sessions}

    application_program_types = {"field": "application_program_type", "title": "Program Type", "options": program_types}

    application_program_levels = {"field": "application_program_level", "title": "Program Level", "options": program_levels}

    application_programs = {"field": "application_program", "title": "Program Applied", "options": programs}

    app_s = Application.objects.all().values('status').distinct()
    statii = AppStatus.objects.filter(code__in=app_s).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    app_statii = {"field": "application_status", "title": "Application Status", "options": statii}

    app_r = Application.objects.all().values('reason').distinct()
    reasons = AppReason.objects.filter(code__in=app_r).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    app_reasons = {"field": "application_reason", "title": "Reason", "options": reasons}

    app_d = Application.objects.all().values('applicant_decision').distinct()
    decisions = AppDecision.objects.filter(code__in=app_d).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    app_decisions = {"field": "application_decision", "title": "Decision", "options": decisions}

    app_a = Application.objects.all().values('action_code').distinct()
    action_codes = AppActionCode.objects.filter(code__in=app_a).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    app_action_codes = {"field": "application_action_code", "title": "Action Code", "options": action_codes}

    application_options.append(application_sessions)
    application_options.append(application_program_levels)
    application_options.append(application_program_types)
    application_options.append(application_programs)
    application_options.append(app_statii)
    application_options.append(app_reasons)
    application_options.append(app_decisions)
    application_options.append(app_action_codes)



    ###
    #  Options for filtering by graduation
    ###
    graduation_options = []

    years = [{"val": x['conferral_period_year']} for x in Graduation.objects.all().values('conferral_period_year').distinct()]
    graduation_years = {"field": "graduation_year", "title": "Conferral Period Year", "options": years}

    months = [{"val": x['conferral_period_month']} for x in Graduation.objects.all().values('conferral_period_month').distinct()]
    graduation_months = {"field": "graduation_month", "title": "Conferral Period Month", "options": months}

    g_s = Graduation.objects.all().values('grad_application_status').distinct()
    g_statii = GradAppStatus.objects.filter(code__in=g_s).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    graduation_statii = {"field": "graduation_status", "title": "Status", "options": g_statii}

    graduation_program_types = {"field": "graduation_program_type", "title": "Program Type", "options": program_types}

    graduation_program_levels = {"field": "graduation_program_level", "title": "Program Level", "options": program_levels}

    graduation_programs = {"field": "graduation_program", "title": "Program Graduating", "options": programs}


    graduation_options.append(graduation_years)
    graduation_options.append(graduation_months)
    graduation_options.append(graduation_statii)
    graduation_options.append(graduation_program_types)
    graduation_options.append(graduation_program_levels)
    graduation_options.append(graduation_programs)


    ###
    #  Options for filtering by awards
    ###
    award_options = []

    award_sessions = {"field": "award_session", "title": "Session", "options": sessions}

    aw_t = Award.objects.all().values('award_type').distinct()
    aw_types = AwardType.objects.filter(code__in=aw_t).filter(hidden=False).annotate(val=F("code"), hover=F('description')).values("val", "hover")
    award_types = {"field": "award_type", "title": "Award Type", "options": aw_types}

    award_options.append(award_sessions)
    award_options.append(award_types)



    grad_years = [x['conferral_period_year'] for x in Graduation.objects.all().order_by('conferral_period_year').values('conferral_period_year').distinct()]
    enroll_sessions = [x['session'] for x in Enroll.objects.all().order_by('session').values('session').distinct()]


    return Response(
        {"enroll_options": enroll_options, 
        "student_options": student_options, 
        "application_options": application_options,
        "graduation_options": graduation_options,
        "award_options": award_options,
        "enroll_sessions": enroll_sessions,
        "grad_years": grad_years
        }
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


class CustomPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data, numbers, geo_collection):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'students': data,
            'numbers': numbers,
            'geo_collection': geo_collection
        })


#
# Takes json with all filter parameters as payload, returns list of students
#
@api_view(['POST'])
def filter_students(request):
    print (request)
    filters = json.loads(request.data['filters'])
    students = Student.objects.all()

    ###
    #  filtering by student details
    ###

    if 'student_province' in filters:
        students = students.filter(province__in=filters['student_province'])

    if 'student_self_id' in filters:
        students = students.filter(self_id__in=filters['student_self_id'])

    if 'student_band_funding' in filters:
        students = students.filter(sponsorship__in=filters['student_band_funding'])

    if 'student_financial_hold' in filters:
        students = students.filter(financial_hold__in=filters['student_financial_hold'])

    ###
    #  filtering by enrollment
    ###

    if 'enroll_session' in filters:
        students = students.filter(enrolls__session__in=filters['enroll_session']).distinct()

    if 'enroll_year_level' in filters:
        students = students.filter(enrolls__year_level__in=filters['enroll_year_level']).distinct()

    if 'enroll_regi_status' in filters:
        students = students.filter(enrolls__regi_status__in=filters['enroll_regi_status']).distinct()

    if 'enroll_sessional_standing' in filters:
        students = students.filter(enrolls__sessional_standing__in=filters['enroll_sessional_standing']).distinct()

    if 'enroll_program_type' in filters:
        students = students.filter(enrolls__program__program_type__in=filters['enroll_program_type']).distinct()

    if 'enroll_program_level' in filters:
        students = students.filter(enrolls__program__level__in=filters['enroll_program_level']).distinct()

    if 'enroll_program' in filters:
        students = students.filter(enrolls__program__in=filters['enroll_program']).distinct()

    if 'enroll_subject' in filters:
        subj_specializations = Specialization.objects.filter(Q(primary_subject__in=filters['enroll_subject']) | Q(secondary_subject__in=filters['enroll_subject']))
        students = students.filter(enrolls__specializations__in=subj_specializations).distinct()

    if 'enroll_specialization' in filters:
        specializations = Specialization.objects.filter(code__in=filters['enroll_specialization'])
        students = students.filter(enrolls__specializations__in=specializations).distinct()

    if 'enroll_average' in filters:
        queries = [Q(enrolls__sessional_average__range=x) for x in filters['enroll_average']]
        query = queries.pop() 
        for item in queries:
            query |= item
        students=students.filter(query).distinct()



    ###
    #  filtering by application
    ###

    if 'application_session' in filters:
        students = students.filter(applications__session__in=filters['application_session']).distinct()

    if 'application_program_type' in filters:
        students = students.filter(applications__program__program_type__in=filters['application_program_type']).distinct()

    if 'application_program_level' in filters:
        students = students.filter(applications__program__level__in=filters['application_program_level']).distinct()

    if 'application_program' in filters:
        students = students.filter(applications__program__in=filters['application_program']).distinct()

    if 'application_status' in filters:
        students = students.filter(applications__status__in=filters['application_status']).distinct()

    if 'application_reason' in filters:
        students = students.filter(applications__reason__in=filters['application_reason']).distinct()

    if 'application_decision' in filters:
        students = students.filter(applications__applicant_decision__in=filters['application_decision']).distinct()

    if 'application_action_code' in filters:
        students = students.filter(applications__action_code__in=filters['application_action_code']).distinct()


    ###
    #  filtering by graduation
    ###

    if 'graduation_program_type' in filters:
        students = students.filter(graduations__program__program_type__in=filters['graduation_program_type']).distinct()

    if 'graduation_program_level' in filters:
        students = students.filter(graduations__program__level__in=filters['graduation_program_level']).distinct()

    if 'graduation_program' in filters:
        students = students.filter(graduations__program__in=filters['graduation_program']).distinct()

    if 'graduation_status' in filters:
        students = students.filter(graduations__grad_application_status__in=filters['graduation_status']).distinct()

    if 'graduation_year' in filters:
        students = students.filter(graduations__conferral_period_year__in=filters['graduation_year']).distinct()

    if 'graduation_month' in filters:
        students = students.filter(graduations__conferral_period_month__in=filters['graduation_month']).distinct()


    ###
    #  filtering by awards
    ###

    if 'award_session' in filters:
        students = students.filter(awards__session__in=filters['award_session']).distinct()

    if 'award_type' in filters:
        students = students.filter(awards__award_type__in=filters['award_type']).distinct()

    if 'award_title' in filters:
        students = students.filter(awards__award_title__icontains=filters['award_title']).distinct()



    ###
    #  search by student number
    ###
    if 'student_number' in filters:
        students = students.filter(student_number=filters['student_number'])


    ###
    #  return list of students
    ###
    if students.count() > 1000:
        return JsonResponse({
            'links': {},
            'count':students.count(),
            'students': '',
            'numbers': '',
            'geo_collection': ''
        })
    else:
        numbers = ''.join(["student_number=" + str(x.student_number) + "&" for x in students])

        student_geom = students.exclude(latcoord__isnull=True).exclude(longcoord__isnull=True)
        points = [Feature(geometry=Point((x.longcoord, x.latcoord)), id=x.student_number, properties={"name":x.__str__()}) for x in student_geom]
        geo_collection = FeatureCollection(points)

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(students, request)

        serializer = StudentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, numbers, geo_collection)


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


def enroll_csv(request):
    params = parse_qs(request.META['QUERY_STRING'])
    session = params['session'][0]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enroll' + str(session) + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['program', 'specialization 1', 'specialization 2', 'students', 'metis', 'first nations', 'inuit'])

    enrolls_in_session = Enroll.objects.filter(session=session, regi_status="REGI").order_by('program')
    if 'health' in params:
        enrolls_in_session = enrolls_in_session.filter(Q(program__is_health=True) | Q(specialization_1__is_health=True))

    enroll_types = enrolls_in_session.values('program', 'specialization_1', 'specialization_2', 'specialization_1__description', 'specialization_2__description').distinct()

    for e_t in enroll_types:
        program = e_t['program']
        spec_1 = e_t['specialization_1']
        spec_2 = e_t['specialization_2']
        total = enrolls_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2).count()
        metis = enrolls_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student__self_id='METI').count()
        f_n = enrolls_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student__self_id='NATI').count()
        inuit = enrolls_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student__self_id='INUI').count()
        row = [program, e_t['specialization_1__description'], e_t['specialization_2__description'], total, metis, f_n, inuit]
        writer.writerow(row)

    return response


def grad_csv(request):
    params = parse_qs(request.META['QUERY_STRING'])
    year = params['year'][0]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grad' + str(year) + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['program', 'specialization 1', 'specialization 2', 'students', 'metis', 'first nations', 'inuit'])
    #TODO: filter by graduation status
    grad_in_session = Graduation.objects.filter(conferral_period_year=year).order_by('program')
    if 'health' in params:
        grad_in_session = grad_in_session.filter(Q(program__is_health=True) | Q(specialization_1__is_health=True))

    grad_types = grad_in_session.values('program', 'specialization_1', 'specialization_2', 'specialization_1__description', 'specialization_2__description').distinct()

    for g_t in grad_types:
        program = g_t['program']
        spec_1 = g_t['specialization_1']
        spec_2 = g_t['specialization_2']
        total = grad_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2).count()
        metis = grad_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student_number__self_id='METI').count()
        f_n = grad_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student_number__self_id='NATI').count()
        inuit = grad_in_session.filter(program=program, specialization_1=spec_1, specialization_2=spec_2, student_number__self_id='INUI').count()
        row = [program, g_t['specialization_1__description'], g_t['specialization_2__description'], total, metis, f_n, inuit]
        writer.writerow(row)

    return response
