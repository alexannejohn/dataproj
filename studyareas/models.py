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


class Program(AbstractModel):
    program = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=100, blank=True, null=True)
    program_type = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.program,)


class Subject(AbstractModel):
    subject_code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.subject_code,)


class Specialization(AbstractModel):
    code = models.IntegerField(primary_key=True)
    program = models.ForeignKey(Program)
    primary_type = models.CharField(max_length=5, blank=True, null=True)
    primary_subject = models.ForeignKey(Subject, blank=True, null=True, related_name="specializations_pri")
    secondary_type = models.CharField(max_length=5, blank=True, null=True)
    secondary_subject = models.ForeignKey(Subject, blank=True, null=True, related_name="specializations_sec")
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.description,)