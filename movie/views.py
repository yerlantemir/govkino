from django.shortcuts import render

# Create your views here.
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import MoviesSerializer
from .models import Movie


class MovieListView(APIView):

    def get(self, request):
        queryset = Movie.objects.all()
        params = request.query_params
        result = queryset

        if 'title' in params:
            result = result.filter(title=params['title'])
        if 'release_date' in params:
            result = result.filter(release_date=params['release_date'])
        serializer = MoviesSerializer(result, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)
