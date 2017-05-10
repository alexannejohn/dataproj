# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20170508_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollspec',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='enrollspec',
            name='enroll',
        ),
        migrations.RemoveField(
            model_name='enrollspec',
            name='subject',
        ),
        migrations.AddField(
            model_name='enroll',
            name='primary_specialization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Specialization'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='program',
            field=models.ForeignKey(default='BSC', on_delete=django.db.models.deletion.CASCADE, to='students.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specialization',
            name='spec_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='EnrollSpec',
        ),
    ]