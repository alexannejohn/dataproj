# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 22:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studyareas', '0005_specialization_is_health'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialization',
            options={'ordering': ['description']},
        ),
    ]
