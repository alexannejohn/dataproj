from django.contrib import admin
from .models import Subject, Program, Specialization
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from students.admin import ExtendedAdmin, ExtendedResource






class ProgramResource(ExtendedResource):

    class Meta:
        model = Program
        import_id_fields = ['program',]


class ProgramAdmin(ExtendedAdmin):
    resource_class = ProgramResource
    list_display = ('program', 'name', 'program_type', 'level')


admin.site.register(Program, ProgramAdmin)


class SpecializationResource(ExtendedResource):

    class Meta:
        model = Specialization
        import_id_fields = ['code',]


class SpecializationAdmin(ExtendedAdmin):
    resource_class = SpecializationResource
    list_display = ('code', 'description', 'program')


admin.site.register(Specialization, SpecializationAdmin)


class SubjectResource(ExtendedResource):

    class Meta:
        model = Subject
        import_id_fields = ['subject_code',]


class SubjectAdmin(ExtendedAdmin):
    resource_class = SubjectResource
    list_display = ('subject_code', 'name')


admin.site.register(Subject, SubjectAdmin)