# Generated by Django 3.2.6 on 2021-08-06 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=75)),
                ('designer', models.CharField(max_length=75)),
                ('year_released', models.IntegerField()),
                ('number_of_players', models.IntegerField()),
                ('duration', models.FloatField()),
                ('age_rec', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('review', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.player')),
            ],
        ),
        migrations.CreateModel(
            name='GameRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.player')),
            ],
        ),
        migrations.CreateModel(
            name='GameImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.player')),
            ],
        ),
        migrations.CreateModel(
            name='GameCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.category')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamer_rater_api.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='categories',
            field=models.ManyToManyField(through='gamer_rater_api.GameCategory', to='gamer_rater_api.Category'),
        ),
    ]