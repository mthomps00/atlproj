# Generated by Django 2.0.7 on 2018-07-25 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0032_auto_20180424_1520'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GDoc',
            new_name='Link',
        ),
        migrations.RenameField(
            model_name='idea',
            old_name='gdocs',
            new_name='links',
        ),
    ]
