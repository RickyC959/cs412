# File: mini_insta/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ProfileListView


urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
