from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # movies = models.ManyToManyField()

    def __str__(self):
        # return self.title
        return str(self.id)


class Movie(models.Model):
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=2048)
    collection = models.ManyToManyField(Collection)
    # genres = models.ManyToManyField(Collection)

    def __str__(self):
        # return self.title
        return str(self.id)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    movie = models.ManyToManyField(Movie)

    def __str__(self):
        # return self.name
        return str(self.id)
