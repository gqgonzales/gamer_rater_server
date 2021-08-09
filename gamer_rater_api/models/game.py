from django.db import models


class Game(models.Model):
    """
    Initializes Game class
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=75)
    designer = models.CharField(max_length=75)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    duration = models.CharField(max_length=50)
    age_rec = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory")

    def __str__(self):
        return self.title
