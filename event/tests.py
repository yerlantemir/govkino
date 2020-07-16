
from datetime import datetime
import json

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Event
from .serializers import EventsSerializer
from movie.models import Movie
from authentication.models import User



# Create your tests here.

class EventNoAuthTestCase(APITestCase):

    def setUp(self):

        self.movies = [
            {"id": "1", "title": "t1", "release_date": timezone.make_aware(datetime(2020, 12, 3)),
             "url": "https://code.djangoproject.com/ticket/13777"},
            {"id": "2", "title": "t2", "release_date": timezone.make_aware(datetime(2020, 3, 2)),
             "url": "https://code.djangoproject.com/ticket/13777"},
            {"id": "3", "title": "t3", "release_date": timezone.make_aware(datetime(2020, 1, 24)),
             "url": "https://code.djangoproject.com/ticket/13777"}]

        temp_movies = []
        for movie_data in self.movies:
            movie = Movie(**movie_data)
            temp_movies.append(movie)
            movie.save()

        user_data = {"username": "yerlantemir", "phone_number": "+77762537792", "password": "12345"}

        self.user = User(**user_data)
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.events = [
            {"title": "t1", "movie": temp_movies[0], "date": timezone.make_aware(datetime(2020, 3, 3, 12, 33)),
             "created_by": self.user},
            {"title": "t2", "movie": temp_movies[1], "date": timezone.make_aware(datetime(2020, 3, 3, 12, 33)),
             "created_by": self.user},
            {"title": "t3", "movie": temp_movies[2], "date": timezone.make_aware(datetime(2020, 3, 3, 12, 33)),
             "created_by": self.user}]
        self.event_models = []
        for event_data in self.events:
            event = Event(**event_data)
            event.save()
            self.event_models.append(event)

    def test_get_events(self):
        response = self.client.get(reverse("getpost"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_events(self):
        data = {"title": "t4", "movie_id": 1, "date": timezone.make_aware(datetime(2020, 11, 3, 4, 5))}
        response = self.client.post(reverse("getpost"), data)

        data2 = {"title": "t4", "movie_id": 1, "date": timezone.make_aware(datetime(2020, 3, 3, 4, 5))}
        response2 = self.client.post(reverse("getpost"), data2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_by_id(self):
        response1 = self.client.get(reverse("detail", kwargs={"pk": self.event_models[0].id}))
        response2 = self.client.get(reverse("detail", kwargs={"pk": self.event_models[1].id}))
        response3 = self.client.get(reverse("detail", kwargs={"pk": 0}))

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

    def test_join_event(self):
        client = self._get_client_with_token()
        before = len(Event.objects.get(pk=self.event_models[0].id).participants.all())

        response = client.put(reverse('detail', kwargs={"pk": self.event_models[0].id}))
        after = len(Event.objects.get(pk=self.event_models[0].id).participants.all())

        self.assertEqual(after - before, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = client.put(reverse('detail', kwargs={"pk": 0}))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_leave_event(self):
        client = self._get_client_with_token()

        client.put(reverse('detail', kwargs={"pk": self.event_models[0].id}))
        before = len(Event.objects.get(pk=self.event_models[0].id).participants.all())
        response = client.delete(reverse('detail', kwargs={"pk": self.event_models[0].id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        after = len(Event.objects.get(pk=self.event_models[0].id).participants.all())
        self.assertEqual(before - after, 1)

    def test_kick_participant(self):
        client = self._get_client_with_token()
        res_of_create = client.put(reverse('detail', kwargs={"pk": self.event_models[0].id}))
        # test create
        self.assertEqual(res_of_create.status_code, status.HTTP_200_OK)
        # test forbidden
        res_of_fake_create = client.post(reverse('config', kwargs={"pk": self.event_models[0].id}))
        self.assertEqual(res_of_fake_create.status_code, status.HTTP_403_FORBIDDEN)

        before = len(Event.objects.get(pk=self.event_models[0].id).participants.all())
        res_of_kick = self.client.post(reverse('config', kwargs={"pk": self.event_models[0].id}),
                                       data={"kickID": client.user.id})
        after = len(Event.objects.get(pk=self.event_models[0].id).participants.all())
        # test kick OK
        self.assertEqual(res_of_kick.status_code, status.HTTP_200_OK)
        # test kick DB OK
        self.assertEqual(after - before, -1)

    def test_update_event(self):
        new_event_data = {'title': 'new title', 'movie_id': self.movies[2]['id'], 'date': '2020-08-20 23:11'}
        event_before = Event.objects.get(pk=self.event_models[0].id)
        res = self.client.put(reverse('config', kwargs={"pk": self.event_models[0].id}), data=new_event_data)
        event_after = Event.objects.get(pk=self.event_models[0].id)

        self.assertNotEqual(event_before.movie, event_after.movie)
        self.assertNotEqual(event_before.title, event_after.title)
        self.assertNotEqual(event_before.date, event_after.date)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        events_len_before = len(Event.objects.filter(closed_at__isnull=True))
        res_of_delete = self.client.delete(reverse('config', kwargs={'pk': self.event_models[0].id}))
        self.assertEqual(res_of_delete.status_code, status.HTTP_204_NO_CONTENT)
        events_len_after = len(Event.objects.filter(closed_at__isnull=True))
        self.assertEqual(events_len_after - events_len_before, -1)

    def _get_client_with_token(self):
        user = User(**{"username": "yerlantemir3", "phone_number": "+77772537792", "password": "12345"})
        user.save()
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        client.user = user

        return client
