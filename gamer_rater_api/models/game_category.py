
from django.db import models
from django.db.models.deletion import CASCADE


class GameCategory(models.Model):
    """
    Join table for assigning categories to games
    """
    game = models.ForeignKey("Game", on_delete=CASCADE)
    category = models.ForeignKey("Category", on_delete=CASCADE)
