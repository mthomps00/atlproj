# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0004_auto_20171014_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='date_updated',
            field=models.DateField(auto_now=True, verbose_name='last updated'),
        ),
        migrations.AlterField(
            model_name='pitch',
            name='date_updated',
            field=models.DateField(auto_now=True, verbose_name='last updated'),
        ),
    ]
