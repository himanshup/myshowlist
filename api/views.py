from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from .models import Entry
from .serializers import EntrySerializer, TokenSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

import json
import requests

# JWT Settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

  def get(self, request, pk=None):
    try:
      user = self.queryset.get(pk=pk)
      total = Entry.objects.all().filter(author_id=pk).count()
      watching = Entry.objects.all().filter(
          author_id=pk).filter(status='watching').count()
      completed = Entry.objects.all().filter(
          author_id=pk).filter(status='completed').count()
      dropped = Entry.objects.all().filter(
          author_id=pk).filter(status='dropped').count()
      planned = Entry.objects.all().filter(
          author_id=pk).filter(status='planned').count()

      data = {}
      data = UserSerializer(user).data
      data['total'] = total
      data['watching'] = watching
      data['completed'] = completed
      data['dropped'] = dropped
      data['planned'] = planned

      return Response(data)
    except User.DoesNotExist:
      return Response(
          data={
              'message': 'User with id: {} does not exist'.format(pk)
          },
          status=status.HTTP_404_NOT_FOUND
      )


class ShowsView(generics.ListAPIView):
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def get(self, request):
    if self.request.query_params.get('q', None):
      q = self.request.query_params.get('q', None)
      url = 'https://api.jikan.moe/v3/search/anime/?q=' + q + '&page=1'
      shows = requests.get(url).json()

      return Response(shows)
    else:
      shows = {}

      airingUrl = 'https://api.jikan.moe/v3/top/anime/1/airing'
      shows['airing'] = requests.get(airingUrl).json()['top']

      upcomingUrl = 'https://api.jikan.moe/v3/top/anime/1/upcoming'
      shows['upcoming'] = requests.get(upcomingUrl).json()['top']

      popularUrl = 'https://api.jikan.moe/v3/top/anime/1/bypopularity'
      shows['popular'] = requests.get(popularUrl).json()['top']

      favoriteUrl = 'https://api.jikan.moe/v3/top/anime/1/favorite'
      shows['favorite'] = requests.get(favoriteUrl).json()['top']

      return Response(shows)


class ShowDetail(generics.RetrieveAPIView):
  serializer_class = EntrySerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def get(self, request, pk=None):
    data = {}

    url = 'https://api.jikan.moe/v3/anime/' + str(pk)
    data['show'] = requests.get(url).json()

    try:
      entry = Entry.objects.filter(author_id=request.user.id).get(malID=pk)
      data['entry'] = EntrySerializer(entry).data
    except Entry.DoesNotExist:
      data['entry'] = None

    return Response(data)


class ListView(generics.ListCreateAPIView):
  queryset = Entry.objects.all()
  serializer_class = EntrySerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def get(self, request, pk=None):
    try:
      entries = self.queryset.filter(author_id=pk)
      return Response(EntrySerializer(entries, many=True).data)
    except User.DoesNotExist:
      return Response(
          data={
              'message': 'User with id: {} does not exist'.format(pk)
          },
          status=status.HTTP_404_NOT_FOUND
      )

  def post(self, request):
    entry = Entry.objects.create(
        malID=int(request.data['malID']),
        title=request.data['title'],
        synopsis=request.data['synopsis'],
        image=request.data['image'],
        year=int(request.data['year']),
        rating=int(request.data['rating']),
        malRating=float(request.data['malRating']),
        episodes=int(request.data['episodes']),
        progress=int(request.data['progress']),
        status=request.data['status'],
        author=self.request.user
    )
    return Response(
        data=EntrySerializer(entry).data,
        status=status.HTTP_201_CREATED
    )


class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Entry.objects.all()
  serializer_class = EntrySerializer
  permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )

  def get(self, request, pk=None, userId=None):
    try:
      entry = self.get_object()
      return Response(EntrySerializer(entry).data)
    except Entry.DoesNotExist:
      return Response(
          data={
              'message': 'Entry with id: {} does not exist'.format(pk)
          },
          status=status.HTTP_404_NOT_FOUND
      )

  def put(self, request, pk=None, userId=None):
    try:
      entry = self.get_object()
      # Send data to update function which is in the serializers file
      updatedEntry = EntrySerializer().update(entry, request.data)
      return Response(EntrySerializer(updatedEntry).data)
    except Entry.DoesNotExist:
      return Response(
          data={
              'message': 'Entry with id: {} does not exist'.format(pk)
          },
          status=status.HTTP_404_NOT_FOUND
      )

  def delete(self, request, pk=None, userId=None):
    try:
      entry = self.get_object()
      entry.delete()
      return Response(
          data={'message': 'Deleted entry!'},
          status=status.HTTP_204_NO_CONTENT
      )
    except Entry.DoesNotExist:
      return Response(
          data={
              'message': 'Entry with id: {} does not exist'.format(pk)
          },
          status=status.HTTP_404_NOT_FOUND
      )


class LoginView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = TokenSerializer
  permission_classes = (permissions.AllowAny,)

  def post(self, request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      # Save user ID in session
      # Also generate and send a token for future calls to the api
      login(request, user)
      serializer = TokenSerializer(data={
          'token': jwt_encode_handler(
              jwt_payload_handler(user)
          )})
      serializer.is_valid()
      return Response(serializer.data)
    else:
      return Response(data={'message': 'Incorrect username or password'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):
    logout(request)
    return Response(data={'message': 'Logged out'})


class RegisterView(generics.CreateAPIView):
  permission_classes = (permissions.AllowAny,)

  def post(self, request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    email = request.data.get("email", "")
    if not username and not password and not email:
      return Response(
          data={
              'message': 'Username, password and email are required'
          },
          status=status.HTTP_400_BAD_REQUEST
      )
    new_user = User.objects.create_user(
        username=username, password=password, email=email
    )
    return Response(
        data=UserSerializer(new_user).data,
        status=status.HTTP_201_CREATED
    )
