# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-02 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0021_auto_20171220_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Not yet approved'), ('ON_OFFER', 'On offer'), ('TENTATIVE', 'Tentative'), ('SCHEDULED', 'Scheduled'), ('COMMITTED', 'Committed'), ('LIVE', 'Live'), ('ARCHIVED', 'Archived'), ('COMPLETED', 'Completed')], default='ON_OFFER', max_length=15),
        ),
    ]
