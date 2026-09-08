# file: quotes/views.py

import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import os

os.environ["TZ"] = "America/New_York"
time.tzset()

# Create your views here.
quotes = ["You have power over your mind - not outside events. Realize this, and you will find strength.",
          "The happiness of your life depends upon the quality of your thoughts.",
          "Waste no more time arguing about what a good man should be. Be one."]
quotesimg = ["img/MarcusAurelius1.jpeg",
             "img/MarcusAurelius2.jpeg",
             "img/MarcusAurelius3.jpeg",]


def home(request):
    '''Define a view to show the 'home.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/quote.html'
    index = random.randint(0, len(quotes)-1)
    # a dict of key/value pairs, to be available for use in template
    context = {
        'quotes': str(quotes[index]),
        'quotesimg': str(quotesimg[index]),
        'current_time': time.ctime(),
    }

    return render(request, template, context)


def quote(request):
    '''Define a view to show the 'quote.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/quote.html'

    # a dict of key/value pairs, to be available for use in template
    index = random.randint(0, len(quotes)-1)
    context = {
        'quotes': str(quotes[index]),
        'quotesimg': str(quotesimg[index]),
        'current_time': time.ctime(),
    }

    return render(request, template, context)


def show_all(request):
    '''Define a view to show the 'show_all.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/show_all.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'quotes': quotes,
        'quotesimg': quotesimg,
        'current_time': time.ctime(),
    }

    return render(request, template, context)


def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/about.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'img': "img/aboutMarcusAurelius.jpeg",
    }

    return render(request, template, context)
