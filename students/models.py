from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.apps import apps
from codetables.models import RegistrationStatus, SessionalStanding
from codetables.models import AwardType, AwardStatus, AppStatus, AppReason, AppDecision, AppReAdmission, AppActionCode, AppMultipleAction
from studyareas.models import Subject, Program, Specialization
from codetables.models import GradAppStatus, GradAppReason
from django.db.models import signals
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from django.contrib.postgres.fields import JSONField



class SavedSearch(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    search_json = JSONField()

    def __str__(self):
        return '%s' % (self.title)



# automatic timestamps for all models
class AbstractModel(models.Model):
    created_by = models.ForeignKey(User, blank=True, null=True, verbose_name='created or edited by')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True


# year and winter/summer
class Session(AbstractModel):
    session = models.CharField(primary_key=True, max_length=5)
    year = models.IntegerField(validators=[MinValueValidator(1111), MaxValueValidator(3000)])
    code = models.CharField(max_length=1)

    class Meta:
        unique_together = (('year', 'code'))
        ordering = ['-session']

    def save(self, *args, **kwargs):
        self.session = str(self.year) + str(self.code)
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.session)


# describes enrollment details for a student in a particular session
class Enroll(AbstractModel):
    student_number = models.ForeignKey('Student', related_name="enrolls", db_index=True)
    session = models.ForeignKey(Session, db_index=True)
    program = models.ForeignKey(Program, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    regi_status = models.ForeignKey(RegistrationStatus, blank=True, null=True)
    sessional_average = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    sessional_standing = models.ForeignKey(SessionalStanding, blank=True, null=True)
    program_entry_year = models.IntegerField(validators=[MinValueValidator(1111), MaxValueValidator(3000)], blank=True, null=True)
    specializations = models.ManyToManyField(Specialization, through='SpecEnrolled', blank=True, null=True)
    #calc values
    specialization_1 = models.ForeignKey(Specialization, blank=True, null=True, related_name="one")
    specialization_2 = models.ForeignKey(Specialization, blank=True, null=True, related_name="two")

    class Meta:
        unique_together = (('student_number', 'session'))

    def __str__(self):
        string = str(self.session) + " - "
        if self.specialization_1 != None:
            string += str(self.specialization_1)
            if self.specialization_2 != None:
                string += ", " + str(self.specialization_2)
        else:
            string += str(self.program)
        return string

    @property
    def regi_status_name(self):
        return self.regi_status.description


def update_recent_enrollment(sender, instance, **kwargs):
    student = instance.student_number
    enroll = student.enrolls.order_by('-session')[0]
    student.most_recent_enrollment = enroll
    student.save(force_update=True)

signals.post_save.connect(update_recent_enrollment, sender=Enroll)



# Many-to-many table between Specialization and Enroll - can be enrolled in multiple specializations at once
class SpecEnrolled(models.Model):
    specialization = models.ForeignKey(Specialization, related_name="specenroll")
    enroll = models.ForeignKey(Enroll, related_name="specenroll")
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = (('enroll', 'order'))

    def __str__(self):
        return '%s %s' % (self.specialization, self.enroll,)


def update_spec(sender, instance, **kwargs):
    enroll = instance.enroll
    if instance.order == 1:
        enroll.specialization_1 = instance.specialization
    elif instance.order == 2:
        enroll.specialization_2 = instance.specialization
    enroll.save(force_update=True)

signals.post_save.connect(update_spec, sender=SpecEnrolled)

# graduation details for a student
class Graduation(AbstractModel):

    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    )


    student_number = models.ForeignKey('Student', related_name="graduations", db_index=True)
    conferral_period = models.DateField()
    conferral_period_year = models.IntegerField(blank=True, null=True)
    conferral_period_month = models.IntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    grad_application_status = models.ForeignKey(GradAppStatus, blank=True, null=True)
    status_reason = models.CharField(max_length=20, blank=True, null=True)
    ceremony_date = models.DateField(blank=True, null=True, db_index=True)
    doctoral_citation = models.CharField(max_length=20, blank=True, null=True)
    dual_degree = models.BooleanField(default=False)
    program = models.ForeignKey(Program)
    specializations = models.ManyToManyField(Specialization, through='SpecGrad', blank=True, null=True)
    #calc values
    specialization_1 = models.ForeignKey(Specialization, blank=True, null=True, related_name="one_g")
    specialization_2 = models.ForeignKey(Specialization, blank=True, null=True, related_name="two_g")

    class Meta:
        unique_together = (('student_number', 'conferral_period', 'program'))

    def save(self, *args, **kwargs):
        self.conferral_period_month = self.conferral_period.month
        self.conferral_period_year = self.conferral_period.year
        super(Graduation, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.program)


# many-to-many field between Specialization and Graduation
class SpecGrad(models.Model):
    specialization = models.ForeignKey(Specialization, related_name="specgrad")
    graduation = models.ForeignKey(Graduation, related_name="specgrad")
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = (('graduation', 'order'))

    def __str__(self):
        return '%s %s' % (self.specialization, self.graduation,)

def update_spec_grad(sender, instance, **kwargs):
    grad = instance.graduation
    if instance.order == 1:
        grad.specialization_1 = instance.specialization
    elif instance.order == 2:
        grad.specialization_2 = instance.specialization
    grad.save(force_update=True)

signals.post_save.connect(update_spec_grad, sender=SpecGrad)


def update_graduation_date(sender, instance, **kwargs):
    student = instance.student_number
    grad = student.graduations.order_by('-ceremony_date')[0]
    student.graduation_date = grad.ceremony_date
    student.save(force_update=True)

signals.post_save.connect(update_graduation_date, sender=Graduation)


# Application details for a student 
class Application(AbstractModel):
    student_number = models.ForeignKey('Student', related_name="applications", db_index=True)
    session = models.ForeignKey(Session, db_index=True)
    program = models.ForeignKey(Program, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    re_admission = models.ForeignKey(AppReAdmission, blank=True, null=True)
    status = models.ForeignKey(AppStatus, blank=True, null=True)
    reason = models.ForeignKey(AppReason, blank=True, null=True)
    applicant_decision = models.ForeignKey(AppDecision, blank=True, null=True)
    action_code = models.ForeignKey(AppActionCode, blank=True, null=True)
    multiple_action = models.ForeignKey(AppMultipleAction, blank=True, null=True)

    class Meta:
        unique_together = (('student_number', 'session'))

    def __str__(self):
        return '%s %s' % (self.program, self.session,)

def update_applied(sender, instance, **kwargs):
    student = instance.student_number
    app = student.applications.order_by('session').values('session')
    student.applied = ",".join([x['session'] for x in app])
    student.save(force_update=True)

signals.post_save.connect(update_applied, sender=Application)

# a student's awards
class Award(AbstractModel):
    student_number = models.ForeignKey('Student', related_name="awards", db_index=True)
    session = models.ForeignKey(Session)
    award_title = models.CharField(max_length=150)
    award_number = models.IntegerField(blank=True, null=True)
    award_amount = models.IntegerField(blank=True, null=True)
    award_type = models.ForeignKey(AwardType, blank=True, null=True)
    status = models.ForeignKey(AwardStatus, blank=True, null=True)

    class Meta:
        unique_together = (('student_number', 'session'))

    def __str__(self):
        return '%s %s' % (self.award_title, self.session,)

def update_award_amount(sender, instance, **kwargs):
    student = instance.student_number
    awards = student.awards.values('award_amount')
    student.total_award_amount = sum([x['award_amount'] for x in awards])
    student.save(force_update=True)

signals.post_save.connect(update_award_amount, sender=Award)


class PreviousInstitution(AbstractModel):
    student_number = models.ForeignKey('Student', related_name="previous_institutions", db_index=True)
    institution_name = models.CharField(max_length=200)
    transfer_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('student_number', 'institution_name'))

    def __str__(self):
        return '%s %s' % (self.student_number, self.institution_name,)


# biographical, contact, and other details
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


    student_number = models.IntegerField(primary_key=True, validators=[MinValueValidator(11111111), MaxValueValidator(99999999)], db_index=True)
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    preferred_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    self_id = models.CharField(max_length=4, blank=True, null=True, choices=SUB_TYPE_CHOICES)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=2, blank=True, null=True, choices=PROVINCE_CHOICES)
    country = models.CharField(max_length=100, blank=True, null=True)

    financial_hold = models.BooleanField(default=False)
    sponsorship = models.BooleanField(default=False)
    sponsorship_start = models.ForeignKey(Session, blank=True, null=True, related_name='spons_start')
    sponsorship_end = models.ForeignKey(Session, blank=True, null=True, related_name='spons_end')
    sponsor = models.CharField(max_length=200, blank=True, null=True)

    #signals??
    first_session_applied = models.ForeignKey(Session, blank=True, null=True, related_name='s_applied')
    first_session_admitted = models.ForeignKey(Session, blank=True, null=True, related_name='s_admitted')
    first_session_registered = models.ForeignKey(Session, blank=True, null=True, related_name='s_reg')

    most_recent_enrollment = models.ForeignKey(Enroll, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    total_award_amount = models.IntegerField(blank=True, null=True)
    applied = models.CharField(max_length=150, blank=True, null=True)
    latcoord = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longcoord = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.city:
            if self.country:
                country = self.country
            else:
                country = 'Canada'
            location = '%s %s %s' % (self.city, self.province, country)

            urlq = {}
            urlq['sensor'] = 'false'
            urlq['address'] = location
            urlq = urlencode(urlq)
            url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urlq

            response = json.loads(urlopen(url).read())
            if response['status'] == 'OK':
                self.latcoord = response['results'][0]['geometry']['location']['lat']
                self.longcoord = response['results'][0]['geometry']['location']['lng']

        super(Student, self).save(*args, **kwargs)


    def __str__(self):
        if self.preferred_name:
            name = self.preferred_name
        else:
            name = self.given_name
        return '%s %s (%s)' % (name, self.surname, self.student_number)








