from django.contrib import admin
from .models import Subject, Program, Specialization
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from students.admin import ExtendedAdmin, ExtendedResource






class ProgramResource(ExtendedResource):

    def before_import_row(self, row, **kwargs):
        if str(row['is_health']).lower() == 'true' or str(row['is_health']).lower() == 'yes':
            row['is_health'] = True

    class Meta:
        model = Program
        import_id_fields = ['program',]


class ProgramAdmin(ExtendedAdmin):
    resource_class = ProgramResource
    list_display = ('program', 'name', 'program_type', 'level', 'is_health')
    search_fields = ('program', 'name')
    list_filter = ('is_health', 'program_type', 'level', 'hidden')


admin.site.register(Program, ProgramAdmin)


class SpecializationResource(ExtendedResource):

    def before_import_row(self, row, **kwargs):
        if str(row['is_health']).lower() == 'true' or str(row['is_health']).lower() == 'yes':
            row['is_health'] = True

    class Meta:
        model = Specialization
        import_id_fields = ['code',]


class SpecializationAdmin(ExtendedAdmin):
    resource_class = SpecializationResource
    list_display = ('code', 'description', 'program', 'is_health')
    search_fields = ('code', 'description', 'primary_subject__subject_code', 'secondary_subject__subject_code')
    list_filter = ('is_health', 'hidden')


admin.site.register(Specialization, SpecializationAdmin)


class SubjectResource(ExtendedResource):

    class Meta:
        model = Subject
        import_id_fields = ['subject_code',]


class SubjectAdmin(ExtendedAdmin):
    resource_class = SubjectResource
    list_display = ('subject_code', 'name')
    search_fields = ('subject_code', 'name')
    list_filter = ('hidden',)


admin.site.register(Subject, SubjectAdmin)