# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-23 23:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20170523_2323'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('student_number', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('student_number', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='graduation',
            unique_together=set([('student_number', 'session')]),
        ),
    ]