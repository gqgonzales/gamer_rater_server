
from django.db import models
from django.db.models.deletion import CASCADE


class GameImage(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    image = models.ImageField()
