
from django.db import models
from django.db.models.deletion import CASCADE


class GameReview(models.Model):
    game = models.ForeignKey("Game", on_delete=CASCADE)
    player = models.ForeignKey("Player", on_delete=CASCADE)
    title = models.CharField(max_length=75)
    review = models.TextField()

    def __str__(self):
        return f'{self.title}, a review'
