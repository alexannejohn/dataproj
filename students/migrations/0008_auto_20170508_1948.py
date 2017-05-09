# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-08 19:48
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0007_program_specialization'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrollSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='enroll',
            name='program_entry_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1111), django.core.validators.MaxValueValidator(3000)]),
        ),
        migrations.AddField(
            model_name='enroll',
            name='regi_status',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='enroll',
            name='sessional_average',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='enroll',
            name='sessional_standing',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='enroll',
            name='year_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Program'),
        ),
        migrations.AlterField(
            model_name='program',
            name='level',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='enrollspec',
            name='enroll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Enroll'),
        ),
        migrations.AddField(
            model_name='enrollspec',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Specialization'),
        ),
    ]
