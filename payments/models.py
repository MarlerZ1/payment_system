from django.contrib.auth.models import AbstractUser
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)


class User(AbstractUser):
    pass