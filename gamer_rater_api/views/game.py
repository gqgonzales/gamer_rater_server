"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamer_rater_api.models import Game, GameCategory, Player, Category
from django.contrib.auth.models import User


class GameView(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        player = Player.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game = Game()
        game.title = request.data["title"]
        game.designer = request.data["designer"]
        game.description = request.data["description"]
        game.number_of_players = request.data["number_of_players"]
        game.year_released = request.data["year_released"]
        game.duration = request.data["duration"]
        game.age_rec = request.data["age_rec"]
        game.player = player

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `category_id` in the body of the request.

        # categories = Category.objects.get(pk=request.data["categories"])
        # game.categories = categories

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            game.categories.set(request.data["categories"])
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            # game.categories.set(request.data["categories"])
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.designer = request.data["designer"]
        game.description = request.data["description"]
        game.number_of_players = request.data["number_of_players"]
        game.year_released = request.data["year_released"]
        game.duration = request.data["duration"]
        game.age_rec = request.data["age_rec"]
        player = Player.objects.get(user=request.auth.user)
        game.player = player

        # Direct assignment to the forward side of a many-to-many set is prohibited.
        # Use categories.set() instead.
        # categories = Category.objects.get(pk=request.data["categories"])
        # game.categories = categories

        try:
            game.save()
            game.categories.set(request.data["categories"])
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Game.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        categories = self.request.query_params.get('type', None)
        if categories is not None:
            games = games.filter(category__id=categories)
        #  This dunderscored id is acting kind of like a join table WHERE statement

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

# The serializer class determines how the Python data should be serialized as JSON to be sent back to the client.


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for default user model"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for Players"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    # player = PlayerSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer',
                  'year_released', 'number_of_players', 'duration', 'age_rec', 'categories', 'player', 'average_rating')
        # fields = ('__all__', 'average_rating')

        depth = 1
        #  Works like EXPAND from JSON Server, exposing a certain number of fields
