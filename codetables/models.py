from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.apps import apps


class AbstractModel(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True, verbose_name='created or edited by')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True

# Enroll
class RegistrationStatus(AbstractModel):
    status_code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.description,)


class SessionalStanding(AbstractModel):
    standing_code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.description,)


class Code(AbstractModel):
    code = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=150, null=True, blank=True)
    hidden = models.BooleanField(default=False)

    class Meta:
       abstract = True

    def __str__(self):
        return '%s' % (self.description,)

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


# Graduation
class GradAppStatus(Code):
    pass

class GradAppReason(Code):
    pass


# allows uploading any documents, in order to include any instructional documents in one place
class Tutorial(models.Model):
    file = models.FileField('File', upload_to='./files/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    def file_link(self):
        if self.file:
            return "<a href='%s'>download</a>" % (self.file.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True

    def __str__(self):
        return '%s' % (self.title,)