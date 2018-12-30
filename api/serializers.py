from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source='author.id')

  class Meta:
    model = Entry
    fields = ('id', 'malID', 'title', 'synopsis', 'image', 'year',
              'rating', 'malRating', 'episodes', 'progress', 'status', 'author')

  def update(self, instance, validated_data):
    instance.rating = validated_data.get('rating', instance.rating)
    instance.progress = validated_data.get('progress', instance.progress)
    instance.status = validated_data.get('status', instance.status)
    instance.save()
    return instance


class TokenSerializer(serializers.Serializer):
  # Serializes token data
  token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'date_joined')
