# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutritrack', '0008_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
