# File: mini_insta/admin.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the models that are registered.

from django.contrib import admin
from .views import *
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
