# File: blog/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/26/2026
# Description:

import random

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article


class ShowAllView(ListView):

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


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
