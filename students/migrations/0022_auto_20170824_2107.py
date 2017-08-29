# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-24 21:07
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0021_auto_20170824_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=models.IntegerField(db_index=True, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999)]),
        ),
    ]