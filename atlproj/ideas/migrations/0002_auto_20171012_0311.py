# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 03:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitch',
            name='date_created',
            field=models.DateField(default=datetime.date.today, verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='pitch',
            name='date_updated',
            field=models.DateField(auto_now=True, verbose_name='date updated'),
        ),
    ]
