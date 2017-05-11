# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-11 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_student_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='province',
            field=models.CharField(blank=True, choices=[('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'), ('NS', 'Nova Scotia'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('ON', 'Ontario'), ('PE', 'Prince Edward Island'), ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon')], max_length=2, null=True),
        ),
    ]
