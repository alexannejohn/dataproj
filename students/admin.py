from django.contrib import admin
from .models import Student, Enroll, Session, SpecEnrolled, Graduation, SpecGrad, Application
from .models import Award, PreviousInstitution, SavedSearch
from studyareas.models import Subject, Program, Specialization
from codetables.models import RegistrationStatus, SessionalStanding
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.core import urlresolvers
from extended_filters.filters import CheckBoxListFilter
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet


# automatically saves user who created/edited object when saving using admin form
class ExtendedAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_by', 'created_on', 'last_modified')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

# automatically saves user who created/edited object when importing from csv
# changes any fields containing whitespace to be None - needs to still be included if overriding before_import_row ie. 
class ExtendedResource(resources.ModelResource):
    user = None

    def before_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        instance.created_by = self.user

    def before_import(self, dataset, dry_run, *args, **kwargs):
        self.user = kwargs['user']
        return super(ExtendedResource, self).before_import(dataset, dry_run, *args, **kwargs)

    def before_import_row(self, row, **kwargs):
        for fieldname, field in row.items():
            if isinstance(field, str):
                if field.isspace() is True:
                    row[fieldname] = None



class StudentResource(ExtendedResource):

    # 'yes' and 'true', any case, all work for boolean True value (False generally blank in csv)
    def before_import_row(self, row, **kwargs):
        if str(row['financial_hold']).lower() == 'true' or str(row['financial_hold']).lower() == 'yes':
            row['financial_hold'] = True
        if str(row['sponsorship']).lower() == 'true' or str(row['sponsorship']).lower() == 'yes':
            row['sponsorship'] = True
        return super(StudentResource, self).before_import_row(row, **kwargs)


    class Meta:
        model = Student
        import_id_fields = ['student_number']

# Inline form for previous institutions
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
    list_display = ('student_number', 'name', 'city', 'get_self_id_display', 'financial_hold', 'sponsorship', 'sponsor', 'enrolled')
    search_fields = ['student_number', 'given_name', 'preferred_name', 'surname', 'email_address', 'sponsor']
    list_filter = ('self_id', 'financial_hold', 'sponsorship')
    inlines = [PreviousInstitutionInline,]
    readonly_fields = ('most_recent_enrollment', 'graduation_date', 'total_award_amount', 'applied', 'latcoord', 'longcoord')

    # create link to enrollment object in admin
    def make_link(self, enroll):
        if enroll:
            link = urlresolvers.reverse("admin:students_enroll_change", args=[enroll.id])
            return u'<a href="%s">%s</a><br>' % (link,str(enroll))
        else:
            return ''

    def enrolled(self, obj):
        return "\n".join([self.make_link(p) for p in obj.enrolls.all()])
    enrolled.allow_tags = True

    # preferred name if exists, otherwise given name
    def name(self, obj):
        if obj.preferred_name:
            name = obj.preferred_name
        else:
            name = obj.given_name
        return name
        
    
admin.site.register(Student, StudentAdmin)


class EnrollResource(ExtendedResource):

    # saving specializations in many-to-many table (EnrollSpec)
    # specialization codes are under headings code_1 and code_2 in csv file, need to be saved to EnrollSpec table

    code_1 = None
    code_2 = None

    def before_import_row(self, row, **kwargs):
        try:
            self.code_1 = int(row['code_1'])
        except (ValueError, TypeError) as e:
            self.code_1 = None
        try:
            self.code_2 = int(row['code_2'])
        except (ValueError, TypeError) as e:
            self.code_2 = None
        return super(EnrollResource, self).before_import_row(row, **kwargs)

    def after_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        SpecEnrolled.objects.filter(enroll=instance).delete()
        if self.code_1 != None:
            specialization = Specialization.objects.get(code=self.code_1)
            enrollspec = SpecEnrolled.objects.create(enroll=instance, specialization=specialization, order=1)
            enrollspec.save()
        if self.code_2 != None:
            specialization = Specialization.objects.get(code=self.code_2)
            enrollspec = SpecEnrolled.objects.create(enroll=instance, specialization=specialization, order=2)
            enrollspec.save()

        return super(EnrollResource, self).after_save_instance(instance, using_transactions, dry_run, *args, **kwargs)

    class Meta:
        model = Enroll
        import_id_fields = ['student_number', 'session']


# Inline form for Specializations

class MyFormSet(BaseInlineFormSet): #giving form access to parent object
    def get_form_kwargs(self, index): 
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs


class SpecEnrolledForm(ModelForm): # if program is saved, can filter specializations

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
    list_display = ('program', 'year_level', 'specialization_1', 'specialization_2', 'session', 'student_number', 'sessional_average')
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'program__program', 'specialization_1__description', 'specialization_2__description']
    readonly_fields = ('created_by', 'created_on', 'last_modified', 'specialization_1', 'specialization_2',)
    ordering = ('student_number', 'session')
    raw_id_fields = ('student_number',)


admin.site.register(Enroll, EnrollAdmin)


class GraduationResource(ExtendedResource):

    # saving specializations in many-to-many table
    # similar to Enroll

    code_1 = None
    code_2 = None

    def before_import_row(self, row, **kwargs):
        try:
            self.code_1 = int(row['code_1'])
        except (ValueError, TypeError) as e:
            self.code_1 = None
        try:
            self.code_2 = int(row['code_2'])
        except (ValueError, TypeError) as e:
            self.code_2 = None
        con_datestr = str(row['conferral_period'])
        cer_datestr = str(row['ceremony_date'])
        row['conferral_period'] = con_datestr[:4] + '-' + con_datestr[4:] + '-01'
        row['ceremony_date'] = cer_datestr[:4] + '-' + cer_datestr[4:] + '-01'
        if str(row['dual_degree']).lower() == 'true' or str(row['dual_degree']).lower() == 'yes':
            row['dual_degree'] = True
        return super(GraduationResource, self).before_import_row(row, **kwargs)

    def after_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        SpecGrad.objects.filter(graduation=instance).delete()
        if self.code_1 != None:
            specialization = Specialization.objects.get(code=self.code_1)
            enrollgrad = SpecGrad.objects.create(graduation=instance, specialization=specialization, order=1)
            enrollgrad.save()
        if self.code_2 != None:
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
        try:
            self.fields['specialization'].queryset = Specialization.objects.filter(program=self.parent_object.program)
        except AttributeError:
            self.fields['specialization'].queryset = Specialization.objects.all()

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
    list_display = ('program', 'student_number', 'grad_application_status', 'status_reason', 'conferral_period_year', 'ceremony_date', 
        'get_conferral_period_month_display',)
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'program__program']
    readonly_fields = ('specialization_1', 'specialization_2',)
    ordering = ('conferral_period_year', 'student_number')
    raw_id_fields = ('student_number',)


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
    raw_id_fields = ('student_number',)


admin.site.register(Application, ApplicationAdmin)


class AwardResource(ExtendedResource):

    class Meta:
        model = Award
        import_id_fields = ['student_number', 'session', 'award_title']


class AwardAdmin(ExtendedAdmin):
    resource_class = AwardResource
    search_fields = ['student_number__student_number', 'student_number__preferred_name',
     'student_number__given_name', 'student_number__surname', 'award_title', 'award_number']
    list_filter = (('status', CheckBoxListFilter), 'session')
    list_display = ('award_title', 'award_number', 'award_amount', 'session', 'student_number', 'status')
    ordering = ('student_number', 'session')
    raw_id_fields = ('student_number',)


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


class SavedSearchAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', 'user')

admin.site.register(SavedSearch, SavedSearchAdmin)


