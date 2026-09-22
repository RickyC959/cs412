# File: restaurant/views.py
# Author: Ricky Cui (rcui1@bu.edu), 9/10/2026
# Description: This page contains any information the page needs. it formats and displays

import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import os

os.environ["TZ"] = "America/New_York"
time.tzset()

# Create your views here.
four_items = {"Seafood Pancake": 15.96,
              "Kimchi Pancake": 14.97,
              "Fish Cake Soup(with sides)": 9.48,
              "Vegetable Pancake": 12.99, }

imgs = ["img/restaurant/fishcake_soup.jpg",
        "img/restaurant/veggie_pancake.jpg",
        ]


def main(request):
    '''Define a view to show the 'main.html' template.'''

    # the template to which we will delegate the work
    template = 'restaurant/main.html'
    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'imgs': imgs,
        'four_items': four_items.items(),
    }

    return render(request, template, context)


def order(request):
    '''Define a view to show the 'order.html' template.'''

    # the template to which we will delegate the work
    template = 'restaurant/order.html'

    context = {
        'current_time': time.ctime(),
        'daily_special': random.choice(list(four_items.items())),
        'four_items': four_items.items(),
    }

    return render(request, template, context)


def confirmation(request):
    print(request.POST)
    if request.POST:
        template_name = 'restaurant/confirmation.html'
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        raw_ordered_items = request.POST.getlist('ordered_items')
        listoforderedfood = []
        total_price = 0.0
        for raw_item in raw_ordered_items:
            # Split the string into the name and the price
            item_name, item_price = raw_item.split('|')

            # Add the name to your list for the confirmation page
            listoforderedfood.append(item_name)

            # Convert the price to a float (decimal) and add to total
            total_price += float(item_price)
        total_price = round(total_price, 2)
        print(listoforderedfood)
        print("Total Price: $", total_price)
        context = {
            'current_time': time.ctime(),
            'ready_time': time.ctime(time.time() + random.randint(1800, 3600)),
            'name': name,
            'phone': phone,
            'email': email,
            'items': listoforderedfood,
            'total_price': total_price,
        }
        return render(request, template_name=template_name, context=context)
