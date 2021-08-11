from django.db import models
from django.db.models.deletion import CASCADE


class GameRating(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.rating}/5 Joysticks'
