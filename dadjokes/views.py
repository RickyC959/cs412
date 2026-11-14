
from dadjokes.serializer import *

from .models import *
from django.views.generic import *
import random
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# '' - show one Joke and one Picture selected at random
# 'random' - show one Joke and one Picture selected at random

# 'jokes' - show a page with all Jokes (no images)
# 'joke/<int:pk>' - show one Joke by its primary key
# 'pictures' - show a page with all Pictures (no jokes)
# 'picture/<int:pk>' - show one Picture by its primary key


class JokeView(DetailView):
    model = Joke
    template_name = "dadjokes/jokeview.html"
    context_object_name = 'joke'


class RandomJokeView(DetailView):
    model = Joke
    template_name = "dadjokes/jokeview.html"
    context_object_name = 'joke'

    def get_object(self):
        all_articles = Joke.objects.all()
        joke = random.choice(all_articles)
        return joke


class ShowAllView(ListView):

    model = Joke
    template_name = "dadjokes/show_all.html"
    context_object_name = "jokes"


def random_joke_and_picture(request):
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())
    context = {
        'joke': random.choice(jokes) if jokes else None,
        'picture': random.choice(pictures) if pictures else None,
    }
    return render(request, 'dadjokes/random.html', context)


class JokeListView(ListView):
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'
    ordering = ['-timestamp']


class JokeDetailView(DetailView):
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'
    ordering = ['-timestamp']


class PictureDetailView(DetailView):
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


# --- REST API Views ---

@api_view(['GET'])
def api_random_joke(request):
    jokes = list(Joke.objects.all())
    if not jokes:
        return Response({'detail': 'No jokes found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = JokeSerializer(random.choice(jokes))
    return Response(serializer.data)


@api_view(['GET'])
def api_random_picture(request):
    pictures = list(Picture.objects.all())
    if not pictures:
        return Response({'detail': 'No pictures found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PictureSerializer(random.choice(pictures))
    return Response(serializer.data)


class JokeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.all().order_by('-timestamp')
    serializer_class = JokeSerializer


class JokeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.all().order_by('-timestamp')
    serializer_class = PictureSerializer


class PictureRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
