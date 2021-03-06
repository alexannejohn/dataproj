# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-23 23:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codetables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradAppReason',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GradAppStatus',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
