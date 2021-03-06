# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-02 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0022_auto_20180102_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Not yet approved'), ('ON_OFFER', 'Available to pitch'), ('TENTATIVE', 'Maybe'), ('SCHEDULED', 'Committed and scheduled'), ('COMMITTED', 'Committed but not yet scheduled'), ('LIVE', 'Currently active'), ('ARCHIVED', 'Archived'), ('COMPLETED', 'Completed')], default='ON_OFFER', max_length=15),
        ),
    ]
