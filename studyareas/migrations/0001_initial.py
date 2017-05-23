# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-23 21:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('program', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('program_type', models.CharField(blank=True, max_length=20, null=True)),
                ('level', models.CharField(blank=True, max_length=20, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('primary_type', models.CharField(blank=True, max_length=5, null=True)),
                ('secondary_type', models.CharField(blank=True, max_length=5, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('subject_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='specialization',
            name='primary_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specializations_pri', to='studyareas.Subject'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studyareas.Program'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='secondary_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specializations_sec', to='studyareas.Subject'),
        ),
    ]
