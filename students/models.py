from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


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


class Specialization(AbstractModel):
    code = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=5)
    name = models.CharField(max_length=100, blank=True, null=True)
    program = models.ForeignKey(Program)
    spec_type = models.CharField(max_length=20, blank=True, null=True) #honours, major

    def __str__(self):
        return '%s' % (self.subject,)



class Enroll(AbstractModel):
    student_number = models.ForeignKey('Student')
    session = models.ForeignKey(Session)
    program = models.ForeignKey(Program, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    regi_status = models.CharField(max_length=5, blank=True, null=True)
    sessional_average = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    sessional_standing = models.CharField(max_length=5, blank=True, null=True)
    program_entry_year = models.IntegerField(validators=[MinValueValidator(1111), MaxValueValidator(3000)], blank=True, null=True)
    specializations = models.ManyToManyField(Specialization, through='SpecEnrolled', blank=True, null=True)

    class Meta:
        unique_together = (('student_number', 'session'))

    def __str__(self):
        return '%s %s' % (self.session, self.program)


class SpecEnrolled(models.Model):
    specialization = models.ForeignKey(Specialization)
    enroll = models.ForeignKey(Enroll)
    pri_sec = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % self.specialization, self.enroll



class Student(AbstractModel):
    SUB_TYPE_CHOICES = (
        ('NATI', 'First Nations'),
        ('INUI', 'Inuit'),
        ('METI', 'Métis'),
    )


    student_number = models.IntegerField(primary_key=True, validators=[MinValueValidator(11111111), MaxValueValidator(99999999)])
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    preferred_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    sub_type = models.CharField(max_length=4, blank=True, null=True, choices=SUB_TYPE_CHOICES)


    def __str__(self):
        return '%s' % (self.given_name)

    @property
    def enrollments(self):
        enrol = Enroll.objects.filter(student_number=self.student_number).order_by('session__year')
        return enrol




