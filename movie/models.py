from django.db import models


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50, unique=True)
    release_date = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, date: {self.release_date}, url: {self.url}'
