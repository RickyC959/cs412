# File: blog/urls.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:
from django.urls import path
from .views import *


urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
]
