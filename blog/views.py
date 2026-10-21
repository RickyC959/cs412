# File: blog/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:

import random

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import *
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ShowAllView(ListView):

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in')
        return super().dispatch(request, *args, **kwargs)


class ArticleView(DetailView):

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


class CreateArticleView(LoginRequiredMixin, CreateView):

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        return reverse('login')

    def form_valid(self, form):
        print(f'CreateArticleViewform_valid(): {form.cleaned_data}')

        user = self.request.user
        print(f'CreateArticleViewform_valid():{user}')
        form.instance.user = user
        return super().form_valid(form)
    

class UpdateArticleView(UpdateView):
    '''A view to update an Article and save it to the database.'''
 
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)
    
class CreateCommentview(CreateView):
    
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse('article', kwargs={'pk': pk})

    def get_context_data(self):

        context = super().get_context_data()

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        context['article'] = article
        return context

    def form_valid(self, form):

        print(form.cleaned_data)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        form.instance.article = article

        return super().form_valid(form)

class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''
 
 
    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
 
 
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})

class UserRegistrationView(CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):


        return reverse('login')