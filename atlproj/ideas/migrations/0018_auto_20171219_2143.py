# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-19 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0017_auto_20171216_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='idea',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='tag',
            name='ideas',
            field=models.ManyToManyField(blank=True, related_name='ideas', related_query_name='idea', to='ideas.Idea'),
        ),
    ]
