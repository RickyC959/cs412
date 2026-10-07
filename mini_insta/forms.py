# File: mini_insta/forms.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: all the forms that are a part of this app

from django import forms 
from .models import * 

class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['caption']

