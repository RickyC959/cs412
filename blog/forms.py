# File: blog/forms.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description: define the forms that we use for create/update/delete operations


from django import forms
from .models import *

class UpdateArticleForm(forms.ModelForm):
    '''A form to update a quote to the database.'''
 
    class Meta:
        '''associate this form with the Article model.'''
        model = Article
        fields = ['title', 'text', ]  # which fields from model should we use
        
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
