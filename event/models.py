from django.db import models

from authentication.models import User
from movie.models import Movie


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(to=User, related_name='participants')
    date = models.DateTimeField(null=True, blank=True)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, movie:{self.movie}'
