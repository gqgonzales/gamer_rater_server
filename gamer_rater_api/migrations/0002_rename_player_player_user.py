# Generated by Django 3.2.6 on 2021-08-06 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_rater_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='player',
            new_name='user',
        ),
    ]
