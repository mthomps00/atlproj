# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0014_auto_20171120_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='workday_title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
