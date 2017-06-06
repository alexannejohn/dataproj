from django.contrib import admin
from .models import Student, Enroll, Session, SpecEnrolled, Graduation, SpecGrad, Application, Award
from studyareas.models import Subject, Program, Specialization
from codetables.models import RegistrationStatus, SessionalStanding
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.core import urlresolvers
from extended_filters.filters import CheckBoxListFilter
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet



class ExtendedAdmin(ImportExportModelAdmin):
    exclude = ('created_by',)


class ExtendedResource(resources.ModelResource):
    user = None

    def before_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        print (self.user)

    def before_import(self, dataset, dry_run, *args, **kwargs):
        self.user = kwargs['user']
        return super(ExtendedResource, self).before_import(dataset, dry_run, *args, **kwargs)


class StudentResource(ExtendedResource):

    class Meta:
        model = Student
        fields = ('student_number', 'given_name')
        import_id_fields = ['student_number']


class StudentAdmin(ExtendedAdmin):
    resource_class = StudentResource
    list_display = ('student_number', 'given_name', 'enrolled')
    search_fields = ['student_number__student_number',]

    def make_link(self, enroll):
        if enroll:
            link = urlresolvers.reverse("admin:students_enroll_change", args=[enroll.id])
            return u'<a href="%s">%s</a><br>' % (link,str(enroll))
        else:
            return ''

    def enrolled(self, obj):
        return "\n".join([self.make_link(p) for p in obj.enrolls.all()])
    enrolled.allow_tags = True
        
    
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
    list_display = ('student_number', 'session', 'program', 'specialization_1', 'specialization_2')
    search_fields = ['student_number__student_number',]


admin.site.register(Enroll, EnrollAdmin)


class GraduationResource(ExtendedResource):

    # saving specializations in many-to-many table

    code_1 = None
    code_2 = None

    def before_import_row(self, row, **kwargs):
        self.code_1 = row['code_1']
        self.code_2 = row['code_2']

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
    list_filter = (('program', CheckBoxListFilter),)
    inlines = (SpecGradInline,)
    list_display = ('student_number', 'program', 'grad_application_status')
    search_fields = ['student_number__student_number',]


admin.site.register(Graduation, GraduationAdmin)


class ApplicationResource(ExtendedResource):

    class Meta:
        model = Application
        import_id_fields = ['student_number', 'session']


class ApplicationAdmin(ExtendedAdmin):
    resource_class = ApplicationResource
    search_fields = ['student_number__student_number',]


admin.site.register(Application, ApplicationAdmin)


class AwardResource(ExtendedResource):

    class Meta:
        model = Award
        import_id_fields = ['student_number', 'session']


class AwardAdmin(ExtendedAdmin):
    resource_class = AwardResource
    search_fields = ['student_number__student_number',]


admin.site.register(Award, AwardAdmin)


class SessionResource(ExtendedResource):

    class Meta:
        model = Session
        import_id_fields = ['year', 'code']


class SessionAdmin(ExtendedAdmin):
    resource_class = SessionResource


admin.site.register(Session, SessionAdmin)


