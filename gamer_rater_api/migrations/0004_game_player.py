# Generated by Django 3.2.6 on 2021-08-13 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_rater_api', '0003_alter_game_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.player'),
            preserve_default=False,
        ),
    ]
