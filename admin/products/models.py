from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)

