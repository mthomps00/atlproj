# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0006_idea_deliverables'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='nickname',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
