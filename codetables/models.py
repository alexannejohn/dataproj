from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.apps import apps


class AbstractModel(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True

# Enroll
class RegistrationStatus(AbstractModel):
    status_code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.status_code,)


class SessionalStanding(AbstractModel):
    standing_code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.standing_code,)


class Code(AbstractModel):
    code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
       abstract = True

# Application
class AppReAdmission(Code):
    pass

class AppStatus(Code):
    pass

class AppReason(Code):
    pass

class AppDecision(Code):
    pass

class AppActionCode(Code):
    pass

class AppMultipleAction(Code):
    pass


# Award
class AwardType(Code):
    pass

class AwardStatus(Code):
    pass