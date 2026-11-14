# File: blog/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 11/12/2026
# Description:
from django.urls import path
from . import views

# '' - show one Joke and one Picture selected at random
# 'random' - show one Joke and one Picture selected at random
# 'jokes' - show a page with all Jokes (no images)
# 'joke/<int:pk>' - show one Joke by its primary key
# 'pictures' - show a page with all Pictures (no jokes)
# 'picture/<int:pk>' - show one Picture by its primary key

urlpatterns = [
    # Web URLs
    path('', views.random_joke_and_picture, name='home'),
    path('random', views.random_joke_and_picture, name='random'),
    path('jokes', views.JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>', views.JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', views.PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>', views.PictureDetailView.as_view(),
         name='picture_detail'),

    # REST API URLs
    path('api/', views.api_random_joke, name='api_home'),
    path('api/random', views.api_random_joke, name='api_random_joke'),
    path('api/jokes', views.JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', views.JokeRetrieveAPIView.as_view(),
         name='api_joke_detail'),
    path('api/pictures', views.PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', views.PictureRetrieveAPIView.as_view(),
         name='api_picture_detail'),
    path('api/random_picture', views.api_random_picture, name='api_random_picture'),



]
