from django.db import models
import uuid


class Collection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movies = models.ManyToManyField('Movie')

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=100)
    uuid = models.UUIDField()

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
