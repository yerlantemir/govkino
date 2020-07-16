from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'username: {self.username}, phone_number: {self.phone_number}'


