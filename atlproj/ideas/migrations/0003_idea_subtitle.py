# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_auto_20171012_0311'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]