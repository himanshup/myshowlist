from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
  malID = models.IntegerField()
  title = models.CharField(max_length=255)
  synopsis = models.TextField()
  image = models.CharField(max_length=255)
  year = models.CharField(max_length=255)
  rating = models.IntegerField()
  malRating = models.FloatField()
  episodes = models.IntegerField()
  progress = models.IntegerField()
  status = models.CharField(max_length=255)
  author = models.ForeignKey(
      'auth.User', related_name='entries', on_delete=models.CASCADE)
