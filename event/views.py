from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_201_CREATED
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from authentication.models import User
from movie.models import Movie
from .serializers import EventsSerializer
from .models import Event


# Create your views here.

# create endpoint
@api_view(['GET', 'POST'])
def event_list(request):
    if not request.user.is_authenticated:
        return Response("Unauthenticated", status=HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        queryset = Event.objects.filter(closed_at__isnull=True)
        serializer = EventsSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    elif request.method == 'POST':
        user_data = request.data

        movie = Movie.objects.get(pk=user_data['movie_id'])
        date = user_data['date'] if 'date' in user_data else None

        serializer = EventsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = Event(title=user_data['title'], date=date, movie=movie, created_by=request.user)
        event.save()
        event.participants.add(request.user)
        event.save()

        return Response(data={"Message": "Event created!"}, status=HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'POST', 'PUT'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(data={"Message": "The event does not exist"}, status=HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = EventsSerializer(event)
        return Response(data=serializer.data, status=HTTP_200_OK)

    # elif request.method == "POST":
    #     event_data = JSONParser().parse(request.data)
    #     serializer = EventsSerializer(event, data=event_data)
    #
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.save()
    #     return Response({"message": "event updated!"}, status=HTTP_200_OK)

    elif request.method == "PUT":
        event.participants.add(request.user)
        event.save()
        return Response({"message": f"{request.user.id} user joined event"}, status=HTTP_200_OK)

    elif request.method == "DELETE":
        event.participants.remove(request.user)
        event.save()
        return Response({"message": f"{request.user.id} user left event"}, status=HTTP_200_OK)


@api_view(['POST', 'PUT', 'DELETE'])
def event_action(request, pk):
    if not request.user.is_authenticated:
        return Response("Unauthenticated", status=HTTP_401_UNAUTHORIZED)

    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(data={"Message": "The event does not exist"}, status=HTTP_404_NOT_FOUND)

    if request.user != event.created_by:
        return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

    if request.method == "POST":
        user = User.objects.get(pk=request.data['kickID'])
        event.participants.remove(user)
        event.save()
        return Response({"message": f"{request.data['kickID']} kicked participant"}, status=HTTP_200_OK)

    elif request.method == "PUT":
        event_data = request.data
        if 'movie_id' in event_data:
            try:
                movie = Movie.objects.get(pk=event_data['movie_id'])
            except Movie.DoesNotExist:
                return Response(data={"Message": "The movie does not exist"}, status=HTTP_404_NOT_FOUND)
            event.movie = movie
            event.save()

        serializer = EventsSerializer(event, data=event_data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"message": f"{pk} event updated!"}, status=HTTP_200_OK)

    elif request.method == "DELETE":
        event.closed_at = timezone.now()
        event.save()
        return Response({"message": f"{pk} event was deleted!"}, status=HTTP_204_NO_CONTENT)
