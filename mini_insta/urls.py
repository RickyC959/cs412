# File: mini_insta/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the URLs that are part of this app

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *
from .forms import *


urlpatterns = [
    path('', ProfileListView.as_view(), name=""),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),

   
    path('post/<int:pk>',  PostDetailView.as_view(), name="show_post"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('post/<int:pk>/like', LikePostView.as_view(), name="like_post"),
    path('post/<int:pk>/delete_like', DeleteLikePostView.as_view(), name="delete_like_post"),

    path('profile/', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/feed', ShowFeedView.as_view(), name="show_feed"),
    path('profile/search',SearchView.as_view(), name="search"),

    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name="follow_profile"),
    path('profile/<int:pk>/delete_follow', DeleteFollowProfileView.as_view(), name="delete_follow_profile"),

    #authloging
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_insta/logged_out.html' ), name="logout"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
