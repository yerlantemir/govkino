from datetime import datetime

from rest_framework import serializers
from django.utils import timezone

from movie.serializers import MoviesSerializer
from authentication.serializers import UsersSerializer
from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    movie = MoviesSerializer(read_only=True)
    participants = UsersSerializer(read_only=True, many=True)
    created_by = UsersSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'participants', 'movie', 'created_by', 'date', 'created_at', 'closed_at']

    def validate_date(self, value):
        if value < timezone.make_aware(datetime.now()):
            raise serializers.ValidationError("Trying to create undated event")
        return value
