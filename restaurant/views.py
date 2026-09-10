# file: restaurant/views.py

import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import os

os.environ["TZ"] = "America/New_York"
time.tzset()

# Create your views here.


def main(request):
    '''Define a view to show the 'main.html' template.'''

    # the template to which we will delegate the work
    template = 'restaurant/'
    # a dict of key/value pairs, to be available for use in template
    context = {

    }

    return render(request, template, context)


def order(request):
    '''Define a view to show the 'order.html' template.'''

    # the template to which we will delegate the work
    template_name = 'restaurant/order.html'

    if request.POST:

        context = {


        }

        return render(request, template_name=template_name, context=context)


def confirmation(request):

    return HttpResponse('''''')
