from django.contrib import admin
from .models import Student, Enroll, Session, SpecEnrolled, Graduation, SpecGrad, Application, Award, PreviousInstitution
from studyareas.models import Subject, Program, Specialization
from codetables.models import RegistrationStatus, SessionalStanding
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.core import urlresolvers
from extended_filters.filters import CheckBoxListFilter
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet



class ExtendedAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_by', 'created_on', 'last_modified')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


class ExtendedResource(resources.ModelResource):
    user = None

    def before_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        print(self.user)
        instance.created_by = self.user

    def before_import(self, dataset, dry_run, *args, **kwargs):
        self.user = kwargs['user']
        return super(ExtendedResource, self).before_import(dataset, dry_run, *args, **kwargs)



class StudentResource(ExtendedResource):

    def before_import_row(self, row, **kwargs):
        if str(row['financial_hold']).lower() == 'true' or str(row['financial_hold']).lower() == 'yes':
            row['financial_hold'] = True
        if str(row['sponsorship']).lower() == 'true' or str(row['sponsorship']).lower() == 'yes':
            row['sponsorship'] = True


    class Meta:
        model = Student
        import_id_fields = ['student_number']


class PIForm(ModelForm):
    class Meta:
        model = PreviousInstitution
        exclude = ('created_by',)


class PreviousInstitutionInline(admin.TabularInline):
    model = PreviousInstitution
    form = PIForm
    extra = 1


class StudentAdmin(ExtendedAdmin):
    resource_class = StudentResource
    list_display = ('student_number', 'name', 'city', 'financial_hold', 'sponsorship', 'sponsor', 'enrolled')
    search_fields = ['student_number', 'given_name', 'preferred_name', 'surname', 'email_address', 'sponsor']
    list_filter = ('self_id', 'financial_hold', 'sponsorship')
    inlines = [PreviousInstitutionInline,]

    def make_link(self, enroll):
        if enroll:
            link = urlresolvers.reverse("admin:students_enroll_change", args=[enroll.id])
            return u'<a href="%s">%s</a><br>' % (link,str(enroll))
        else:
            return ''

    def enrolled(self, obj):
        return "\n".join([self.make_link(p) for p in obj.enrolls.all()])
    enrolled.allow_tags = True

    def name(self, obj):
        if obj.preferred_name:
            name = obj.preferred_name
        else:
            name = obj.given_name
        return name
        
    
admin.site.register(Student, StudentAdmin)


class EnrollResource(ExtendedResource):

    # saving specializations in many-to-many table

    code_1 = None
    code_2 = None

    def before_import_row(self, row, **kwargs):
        self.code_1 = row['code_1']
        self.code_2 = row['code_2']

    def after_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        SpecEnrolled.objects.filter(enroll=instance).delete()
        if self.code_1 != None and len(self.code_1) > 0:
            specialization = Specialization.objects.get(code=self.code_1)
            enrollspec = SpecEnrolled.objects.create(enroll=instance, specialization=specialization, order=1)
            enrollspec.save()
        if self.code_2 != None and len(self.code_2) > 0:
            specialization = Specialization.objects.get(code=self.code_2)
            enrollspec = SpecEnrolled.objects.create(enroll=instance, specialization=specialization, order=2)
            enrollspec.save()

        return super(EnrollResource, self).after_save_instance(instance, using_transactions, dry_run, *args, **kwargs)

    class Meta:
        model = Enroll
        import_id_fields = ['student_number', 'session']

class MyFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs


class SpecEnrolledForm(ModelForm):

    def __init__(self, *args, parent_object, **kwargs): 
        self.parent_object = parent_object     
        super(SpecEnrolledForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].queryset = Specialization.objects.filter(program=self.parent_object.program)


class SpecEnrolledInline(admin.TabularInline):
    model = SpecEnrolled
    formset = MyFormSet
    form = SpecEnrolledForm
    extra = 1 # how many rows to show


class EnrollAdmin(ExtendedAdmin):
    resource_class = EnrollResource
    list_filter = (('session', CheckBoxListFilter), ('program', CheckBoxListFilter))
    inlines = (SpecEnrolledInline,)
    list_display = ('program', 'specialization_1', 'specialization_2', 'session', 'student_number', 'sessional_average')
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'program__program', 'specialization_1__description', 'specialization_2__description']
    readonly_fields = ('created_by', 'created_on', 'last_modified', 'specialization_1', 'specialization_2',)
    ordering = ('student_number', 'session')


admin.site.register(Enroll, EnrollAdmin)


class GraduationResource(ExtendedResource):

    # saving specializations in many-to-many table

    code_1 = None
    code_2 = None

    def before_import_row(self, row, **kwargs):
        self.code_1 = row['code_1']
        self.code_2 = row['code_2']
        row['conferral_period'] = str(row['conferral_period']) + "-01"
        if str(row['dual_degree']).lower() == 'true' or str(row['dual_degree']).lower() == 'yes':
            row['dual_degree'] = True

    def after_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        SpecGrad.objects.filter(graduation=instance).delete()
        if self.code_1 != None and len(self.code_1) > 0:
            specialization = Specialization.objects.get(code=self.code_1)
            enrollgrad = SpecGrad.objects.create(graduation=instance, specialization=specialization, order=1)
            enrollgrad.save()
        if self.code_2 != None and len(self.code_2) > 0:
            specialization = Specialization.objects.get(code=self.code_2)
            enrollgrad = SpecGrad.objects.create(graduation=instance, specialization=specialization, order=2)
            enrollgrad.save()

        return super(GraduationResource, self).after_save_instance(instance, using_transactions, dry_run, *args, **kwargs)

    class Meta:
        model = Graduation
        import_id_fields = ['student_number', 'conferral_period', 'program']

class SpecGradForm(ModelForm):

    def __init__(self, *args, parent_object, **kwargs): 
        self.parent_object = parent_object     
        super(SpecGradForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].queryset = Specialization.objects.filter(program=self.parent_object.program)


class SpecGradInline(admin.TabularInline):
    model = SpecGrad
    formset = MyFormSet
    form = SpecGradForm
    extra = 1 # how many rows to show


class GraduationAdmin(ExtendedAdmin):
    resource_class = GraduationResource
    list_filter = (('conferral_period_year', CheckBoxListFilter), ('grad_application_status', CheckBoxListFilter), 
        ('status_reason', CheckBoxListFilter), ('program', CheckBoxListFilter),)
    inlines = (SpecGradInline,)
    list_display = ('program', 'student_number', 'grad_application_status', 'status_reason', 'conferral_period_year', 
        'get_conferral_period_month_display',)
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'program__program']
    readonly_fields = ('specialization_1', 'specialization_2',)
    ordering = ('conferral_period_year', 'student_number')


admin.site.register(Graduation, GraduationAdmin)


class ApplicationResource(ExtendedResource):

    class Meta:
        model = Application
        import_id_fields = ['student_number', 'session']


class ApplicationAdmin(ExtendedAdmin):
    resource_class = ApplicationResource
    list_display = ('program', 'session', 'year_level', 'student_number', 'status', 'applicant_decision')
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'program__program', 'session__session']
    list_filter = ('session', ('status', CheckBoxListFilter), ('applicant_decision', CheckBoxListFilter), ('program', CheckBoxListFilter),)
    ordering = ('student_number', 'session')


admin.site.register(Application, ApplicationAdmin)


class AwardResource(ExtendedResource):

    class Meta:
        model = Award
        import_id_fields = ['student_number', 'session']


class AwardAdmin(ExtendedAdmin):
    resource_class = AwardResource
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'award_title', 'award_number']
    list_filter = (('status', CheckBoxListFilter), 'session')
    list_display = ('award_title', 'award_number', 'award_amount', 'session', 'student_number', 'status')
    ordering = ('student_number', 'session')


admin.site.register(Award, AwardAdmin)


class SessionResource(ExtendedResource):

    class Meta:
        model = Session
        import_id_fields = ['year', 'code']


class SessionAdmin(ExtendedAdmin):
    resource_class = SessionResource


admin.site.register(Session, SessionAdmin)


class PreviousInstitutionResource(ExtendedResource):

    class Meta:
        model = PreviousInstitution
        import_id_fields = ['student_number', 'institution_name']


class PreviousInstitutionAdmin(ExtendedAdmin):
    resource_class = PreviousInstitutionResource
    list_display = ('student_number', 'institution_name', 'transfer_credits')
    search_fields = ['student_number__student_number',]


admin.site.register(PreviousInstitution, PreviousInstitutionAdmin)


