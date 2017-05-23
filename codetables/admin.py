from django.contrib import admin
from .models import RegistrationStatus, SessionalStanding
from .models import AwardType, AwardStatus, AppStatus, AppReason, AppDecision, AppReAdmission, AppActionCode, AppMultipleAction
from .models import GradAppStatus, GradAppReason
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


class AwardTypeResource(ExtendedResource):
    class Meta:
        model = AwardType
        import_id_fields = ['code',]

class AwardTypeAdmin(ExtendedAdmin):
    resource_class = AwardTypeResource
    list_display = ('code', 'description')

admin.site.register(AwardType, AwardTypeAdmin)


class AwardStatusResource(ExtendedResource):
    class Meta:
        model = AwardStatus
        import_id_fields = ['code',]

class AwardStatusAdmin(ExtendedAdmin):
    resource_class = AwardStatusResource
    list_display = ('code', 'description')

admin.site.register(AwardStatus, AwardStatusAdmin)


class AppStatusResource(ExtendedResource):
    class Meta:
        model = AppStatus
        import_id_fields = ['code',]

class AppStatusAdmin(ExtendedAdmin):
    resource_class = AppStatusResource
    list_display = ('code', 'description')

admin.site.register(AppStatus, AppStatusAdmin)


class AppReasonResource(ExtendedResource):
    class Meta:
        model = AppReason
        import_id_fields = ['code',]

class AppReasonAdmin(ExtendedAdmin):
    resource_class = AppReasonResource
    list_display = ('code', 'description')

admin.site.register(AppReason, AppReasonAdmin)


class AppDecisionResource(ExtendedResource):
    class Meta:
        model = AppDecision
        import_id_fields = ['code',]

class AppDecisionAdmin(ExtendedAdmin):
    resource_class = AppDecisionResource
    list_display = ('code', 'description')

admin.site.register(AppDecision, AppDecisionAdmin)


class AppReAdmissionResource(ExtendedResource):
    class Meta:
        model = AppReAdmission
        import_id_fields = ['code',]

class AppReAdmissionAdmin(ExtendedAdmin):
    resource_class = AppReAdmissionResource
    list_display = ('code', 'description')

admin.site.register(AppReAdmission, AppReAdmissionAdmin)


class AppActionCodeResource(ExtendedResource):
    class Meta:
        model = AppActionCode
        import_id_fields = ['code',]

class AppActionCodeAdmin(ExtendedAdmin):
    resource_class = AppActionCodeResource
    list_display = ('code', 'description')

admin.site.register(AppActionCode, AppActionCodeAdmin)


class AppMultipleActionResource(ExtendedResource):
    class Meta:
        model = AppMultipleAction
        import_id_fields = ['code',]

class AppMultipleActionAdmin(ExtendedAdmin):
    resource_class = AppMultipleActionResource
    list_display = ('code', 'description')

admin.site.register(AppMultipleAction, AppMultipleActionAdmin)


class GradAppStatusResource(ExtendedResource):
    class Meta:
        model = GradAppStatus
        import_id_fields = ['code',]

class GradAppStatusAdmin(ExtendedAdmin):
    resource_class = GradAppStatusResource
    list_display = ('code', 'description')

admin.site.register(GradAppStatus, GradAppStatusAdmin)


class GradAppReasonResource(ExtendedResource):
    class Meta:
        model = GradAppReason
        import_id_fields = ['code',]

class GradAppReasonAdmin(ExtendedAdmin):
    resource_class = GradAppReasonResource
    list_display = ('code', 'description')

admin.site.register(GradAppReason, GradAppReasonAdmin)



