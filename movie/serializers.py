from rest_framework import serializers
from .models import Movie


class MoviesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'url']