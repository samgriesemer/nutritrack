# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutritrack', '0004_auto_20171028_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='description',
            field=models.TextField(default=''),
        ),
    ]