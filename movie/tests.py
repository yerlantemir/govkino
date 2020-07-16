from django.test import TestCase

# Create your tests here.


from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from authentication.models import User


# Create your tests here.

class MovieViews(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_movie_list_view(self):
        res_get_movies = self.client.get(reverse('get_movies'))
        self.assertEqual(res_get_movies.status_code, status.HTTP_200_OK)

