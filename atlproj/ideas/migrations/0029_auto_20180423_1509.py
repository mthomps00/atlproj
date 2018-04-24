# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-23 15:09
from __future__ import unicode_literals

from django.db import models, migrations

def forward(apps,schema_editor):
    Pitch = apps.get_model('ideas', 'Pitch')
    PitchMeta = apps.get_model('ideas', 'PitchMeta')
    for pitch in Pitch.objects.all():
        meta = PitchMeta.objects.create(pitch=pitch, idea=pitch.idea)

def reverse(apps,schema_editor):
    PitchMeta = apps.get_model('ideas', 'PitchMeta')
    for meta in PitchMeta.objects.all():
        ideas = meta.pitch.ideas.add(meta.idea)

class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0028_auto_20180423_1451'),
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
