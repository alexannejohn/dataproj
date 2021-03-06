# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-25 20:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_savedsearch'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sponsorship_end',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spons_end', to='students.Session'),
        ),
        migrations.AddField(
            model_name='student',
            name='sponsorship_start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spons_start', to='students.Session'),
        ),
    ]
