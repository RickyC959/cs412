# File: mini_insta/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.


class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"
