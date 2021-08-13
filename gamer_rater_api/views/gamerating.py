"""View module for handling rating requests"""
from gamer_rater_api.models.game_rating import GameRating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import fields
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamer_rater_api.models import GameRating, Game, Player


class GameRatingView(ViewSet):
    """Game rater Ratings view!"""

    def list(self, request):
        """Handle GET requests to GameRating resource
        Returns:
            Response -- JSON serialized list of ratings
        """
        # Get all rating records from the database
        game = self.request.query_params.get('game', None)

        # if game is not None:
        #     ratings = GameRating.objects.filter(game=game)

        if game:
            ratings = GameRating.objects.filter(game=game)
        else:
            ratings = GameRating.objects.all()

        serializer = GameRatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating instance
        """
        try:
            rating = GameRating.objects.get(pk=pk)
            serializer = GameRatingSerializer(
                rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations for new ratings
        Returns:
            Response -- JSON serialized game instance
        """

        rating = GameRating()

        game = Game.objects.get(pk=request.data["game"])
        rating.game = game

        player = Player.objects.get(user=request.auth.user)
        rating.player = player

        rating.rating = request.data["rating"]

        try:
            rating.save()
            serializer = GameRatingSerializer(
                rating, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Games"""

    class Meta:
        """DOCSTRING FILLER"""
        model = Game
        fields = ('id', 'title', 'categories')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event host's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for Players"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']


class GameRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for ratings
    Arguments: serializer game
    """
    player = PlayerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = GameRating
        fields = '__all__'
        depth = 1
