# File: mini_insta/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the URLs that are part of this app

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [
    path('', ProfileListView.as_view(), name=""),
    path('show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="photo"),
    path('post/<int:pk>',  PostDetailView.as_view(), name="post"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
