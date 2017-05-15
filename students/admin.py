from django.contrib import admin
from .models import Student, Enroll, Session, Program, Specialization, SpecEnrolled
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

    def make_link(self, enroll):
        if enroll:
            link = urlresolvers.reverse("admin:students_enroll_change", args=[enroll.id])
            return u'<a href="%s">%s</a><br>' % (link,str(enroll))
        else:
            return ''

    def enrolled(self, obj):
        return "\n".join([self.make_link(p) for p in obj.enrollments.all()])
    enrolled.allow_tags = True
        
    
admin.site.register(Student, StudentAdmin)


class EnrollResource(ExtendedResource):

    code_1 = None

    def before_import_row(self, row, **kwargs):
        self.code_1 = row['code_1']

    def after_save_instance(self, instance, using_transactions, dry_run, *args, **kwargs):
        if len(self.code_1) > 0:
            specialization = Specialization.objects.get(code=self.code_1)
            enrollspec = SpecEnrolled.objects.create(enroll=instance, specialization=specialization, pri_sec="PRI")
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


admin.site.register(Enroll, EnrollAdmin)


class SessionResource(ExtendedResource):

    class Meta:
        model = Session
        import_id_fields = ['year', 'code']


class SessionAdmin(ExtendedAdmin):
    resource_class = SessionResource


admin.site.register(Session, SessionAdmin)


class ProgramResource(ExtendedResource):

    class Meta:
        model = Program
        import_id_fields = ['program',]


class ProgramAdmin(ExtendedAdmin):
    resource_class = ProgramResource
    list_display = ('program', 'name',)


admin.site.register(Program, ProgramAdmin)


class SpecializationResource(ExtendedResource):

    class Meta:
        model = Specialization
        import_id_fields = ['code',]


class SpecializationAdmin(ExtendedAdmin):
    resource_class = SpecializationResource
    list_display = ('code', 'description', 'program')


admin.site.register(Specialization, SpecializationAdmin)


