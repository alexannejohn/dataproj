from rest_framework import serializers
from .models import Student, Enroll, Application, Graduation, Award, PreviousInstitution, SavedSearch

# 
# Serializers for detailed information on one student
#
class EnrollSerializer(serializers.ModelSerializer):
    specialization_1 = serializers.StringRelatedField()
    specialization_2 = serializers.StringRelatedField()
    regi_status = serializers.StringRelatedField()
    sessional_standing = serializers.StringRelatedField()

    class Meta:
        model = Enroll
        fields = ('session', 'program', 'specialization_1', 
            'specialization_2', 'year_level', 'sessional_standing', 'regi_status',
            'sessional_average')

class ApplicationSerializer(serializers.ModelSerializer):
    re_admission = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    reason = serializers.StringRelatedField()
    applicant_decision = serializers.StringRelatedField()
    action_code = serializers.StringRelatedField()
    multiple_action = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ('session', 'program', 'year_level', 're_admission', 'status', 'reason', 
            'applicant_decision', 'action_code', 'multiple_action')


class GraduationSerializer(serializers.ModelSerializer):
    specialization_1 = serializers.StringRelatedField()
    specialization_2 = serializers.StringRelatedField()
    class Meta:
        model = Graduation
        fields = ('program', 'ceremony_date', 'conferral_period_year', 'conferral_period_month', 
            'grad_application_status', 'status_reason', 'doctoral_citation', 'dual_degree', 
            'specialization_1', 'specialization_2')

class AwardSerializer(serializers.ModelSerializer):
    award_type = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    
    class Meta:
        model = Award
        fields = ('session', 'award_title', 'award_amount', 'award_number',
            'award_type', 'status')

class PreviousInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousInstitution
        fields = ('institution_name', 'transfer_credits')


class StudentDetailSerializer(serializers.ModelSerializer):
    enrolls = EnrollSerializer(read_only=True, many=True)
    applications = ApplicationSerializer(read_only=True, many=True)
    graduations = GraduationSerializer(read_only=True, many=True)
    awards = AwardSerializer(read_only=True, many=True)
    previous_institutions = PreviousInstitutionSerializer(read_only=True, many=True)

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'surname', 'preferred_name', 'gender', 'birthdate',
            'self_id', 'city', 'province', 'country', 'financial_hold', 'sponsorship',
            'sponsorship_start', 'sponsorship_end', 'sponsor',
            'enrolls', 'applications', 'graduations', 'awards', 'province', 'previous_institutions')

# Serializer for list of students
class StudentSerializer(serializers.ModelSerializer):
    most_recent_enrollment = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ('student_number', 'given_name', 'preferred_name', 'surname', 'most_recent_enrollment', 'graduation_date', 
            'applied', 'total_award_amount', 'sponsorship', 'sponsor')

# Serializer for list of saved searches
class SavedSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedSearch
        fields = ('title', 'created_on', 'search_json', 'id')
