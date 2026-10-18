# File: mini_insta/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the URLs that are part of this app

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from .forms import *


urlpatterns = [
    path('', ProfileListView.as_view(), name=""),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>',  PostDetailView.as_view(), name="show_post"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/feed', ShowFeedView.as_view(), name="show_feed"),
    path('profile/<int:pk>/search',SearchView.as_view(), name="search"),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
