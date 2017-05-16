from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.apps import apps


# Create your models here.

class AbstractModel(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True


class Session(AbstractModel):
    session = models.CharField(primary_key=True, max_length=5)
    year = models.IntegerField(validators=[MinValueValidator(1111), MaxValueValidator(3000)])
    code = models.CharField(max_length=1)

    class Meta:
        unique_together = (('year', 'code'))

    def save(self, *args, **kwargs):
        self.session = str(self.year) + str(self.code)
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.session)


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
    primary_subject = models.ForeignKey(Subject, blank=True, null=True, related_name="specializations_pri")
    secondary_type = models.CharField(max_length=5, blank=True, null=True)
    secondary_subject = models.ForeignKey(Subject, blank=True, null=True, related_name="specializations_sec")
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.description,)


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


class Enroll(AbstractModel):
    student_number = models.ForeignKey('Student')
    session = models.ForeignKey(Session)
    program = models.ForeignKey(Program, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    regi_status = models.ForeignKey(RegistrationStatus, blank=True, null=True)
    sessional_average = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    sessional_standing = models.ForeignKey(SessionalStanding, blank=True, null=True)
    program_entry_year = models.IntegerField(validators=[MinValueValidator(1111), MaxValueValidator(3000)], blank=True, null=True)
    specializations = models.ManyToManyField(Specialization, through='SpecEnrolled', blank=True, null=True)

    class Meta:
        unique_together = (('student_number', 'session'))

    def __str__(self):
        return '%s %s' % (self.session, self.program)

    @property
    def specialization_1(self):
        e_s = apps.get_model(app_label='students', model_name='SpecEnrolled')\
            .objects.filter(enroll=self, order=1)
        if len(e_s) > 0:
            return e_s[0].specialization
        else:
            return None

    @property
    def specialization_2(self):
        e_s = apps.get_model(app_label='students', model_name='SpecEnrolled')\
            .objects.filter(enroll=self, order=2)
        if len(e_s) > 0:
            return e_s[0].specialization
        else:
            return None

    @property
    def regi_status_name(self):
        return self.regi_status.description


class SpecEnrolled(models.Model):
    specialization = models.ForeignKey(Specialization)
    enroll = models.ForeignKey(Enroll)
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = (('enroll', 'order'))

    def __str__(self):
        return '%s %s' % (self.specialization, self.enroll,)


# class Graduation(AbstractModel):
#     student_number = models.ForeignKey('Student')
#     #first session applied
#     #first session admitted
#     #first session registered
#     grad_application_status = models.CharField(max_length=10)
#     status_reason = models.CharField(max_length=50, blank=True, null=True)
#     transfer_credits = models.CharField(max_length=40, blank=True, null=True)
#     program, specialization




class Student(AbstractModel):
    SUB_TYPE_CHOICES = (
        ('NATI', 'First Nations'),
        ('INUI', 'Inuit'),
        ('METI', 'Métis'),
    )

    PROVINCE_CHOICES = (
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NS', 'Nova Scotia'),
        ('NT', 'Northwest Territories'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon')
    )


    student_number = models.IntegerField(primary_key=True, validators=[MinValueValidator(11111111), MaxValueValidator(99999999)])
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    preferred_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    sub_type = models.CharField(max_length=4, blank=True, null=True, choices=SUB_TYPE_CHOICES)
    province = models.CharField(max_length=2, blank=True, null=True, choices=PROVINCE_CHOICES)


    def __str__(self):
        return '%s' % (self.given_name)

    @property
    def enrollments(self):
        enrol = Enroll.objects.filter(student_number=self.student_number).order_by('session__year')
        return enrol





