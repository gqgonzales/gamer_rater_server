from django.contrib import admin
from gamer_rater_api.models import Game, Category, GameCategory, GameReview, GameImage, GameRating

# Register your models here.
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(GameCategory)
admin.site.register(GameReview)
admin.site.register(GameImage)
admin.site.register(GameRating)
