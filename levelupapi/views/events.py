from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer

class EventView(ViewSet):
    """View for handling requests about events"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single event by ID"""
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events"""
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations"""
        game = Game.objects.get(pk=request.data["gameId"]) 
        organizer = Gamer.objects.get(uid=request.data["organizerId"])  

        event = Event.objects.create(
            game=game,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=organizer,
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an event"""
        event = Event.objects.get(pk=pk)

        event.game_id = request.data.get("gameId", event.game_id)
        event.organizer_id = request.data.get("organizerId", event.organizer_id)
        event.description = request.data.get("description", event.description)
        event.date = request.data.get("date", event.date)
        event.time = request.data.get("time", event.time)

        event.save()

        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
