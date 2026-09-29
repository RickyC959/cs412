# File: mini_insta/admin.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:

from django.contrib import admin
from .views import Profile

# Register your models here.
admin.site.register(Profile)
