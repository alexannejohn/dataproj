from django.contrib import admin
from .models import RegistrationStatus, SessionalStanding
from .models import AwardType, AwardStatus, AppStatus, AppReason, AppDecision, AppReAdmission, AppActionCode, AppMultipleAction
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from students.admin import ExtendedAdmin, ExtendedResource



class RegistrationStatusResource(ExtendedResource):

    class Meta:
        model = RegistrationStatus
        import_id_fields = ['status_code',]


class RegistrationStatusAdmin(ExtendedAdmin):
    resource_class = RegistrationStatusResource
    list_display = ('status_code', 'description')


admin.site.register(RegistrationStatus, RegistrationStatusAdmin)


class SessionalStandingResource(ExtendedResource):

    class Meta:
        model = SessionalStanding
        import_id_fields = ['standing_code',]


class SessionalStandingAdmin(ExtendedAdmin):
    resource_class = SessionalStandingResource
    list_display = ('standing_code', 'description')


admin.site.register(SessionalStanding, SessionalStandingAdmin)
