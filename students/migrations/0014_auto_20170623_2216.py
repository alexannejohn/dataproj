# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20170615_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-session']},
        ),
        migrations.AlterField(
            model_name='graduation',
            name='conferral_period_month',
            field=models.IntegerField(blank=True, choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], null=True),
        ),
    ]
