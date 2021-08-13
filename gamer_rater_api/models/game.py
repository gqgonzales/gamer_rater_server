from gamer_rater_api.models.game_rating import GameRating
from django.db import models
# from django.contrib.auth.models import User


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

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        if len(ratings):
            return total_rating / len(ratings)

        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.

    @average_rating.setter
    def joined(self, value):
        self.__average_rating = value
