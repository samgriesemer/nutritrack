# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutritrack', '0010_auto_20171029_0511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='nutrients',
        ),
        migrations.AddField(
            model_name='meal',
            name='nutrients',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='nutritrack.Nutrient'),
        ),
    ]