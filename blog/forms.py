# File: blog/forms.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: define the forms that we use for create/update/delete operations


from django import forms
from .models import *


class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['author', 'text']
