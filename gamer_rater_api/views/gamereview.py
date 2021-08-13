"""View module for handling review requests"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import fields
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamer_rater_api.models import GameReview, Game, Player


class GameReviewView(ViewSet):
    """Game rater GameReview"""

    def list(self, request):
        """Handle GET requests to GameReview resource
        Returns:
            Response -- JSON serialized list of reviews
        """
        # Get all review records from the database
        game = self.request.query_params.get('game', None)

        # if game is not None:
        #     reviews = GameReview.objects.filter(game=game)

        if game:
            reviews = GameReview.objects.filter(game=game)
        else:
            reviews = GameReview.objects.all()

        serializer = GameReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review instance
        """
        try:
            review = GameReview.objects.get(pk=pk)
            serializer = GameReviewSerializer(
                review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """

        review = GameReview()

        review.title = request.data["title"]
        review.review = request.data["review"]

        game = Game.objects.get(pk=request.data["game"])
        review.game = game

        player = Player.objects.get(user=request.auth.user)
        review.player = player

        try:
            review.save()
            serializer = GameReviewSerializer(
                review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class GameSerializer(serializers.ModelSerializer):
    """SErializer for Games"""

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
    """JSON serializer for event host"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']


class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews
    Arguments: serializer game
    """
    player = PlayerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = GameReview
        fields = '__all__'
        depth = 1
