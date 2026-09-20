# file: formdata/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def show_form(request):
    '''Define a view to show the 'form.html' template.'''

    # the template to which we will delegate the work
    template = 'formdata/form.html'

    # a dict of key/value pairs, to be available for use in template
    context = {

    }

    return render(request, template, context)


def submit(request):

    print(request.POST)

    if request.POST:
        template_name = "formdata/confirmation.html"
        name = request.POST['name']
        fav_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color': fav_color,

        }

    return render(request, template_name=template_name, context=context)
