# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20170510_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
