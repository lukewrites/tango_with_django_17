from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page


def index(request):
    """Query the database for a list of ALL categories
    Order the categories by number of likes in descending order.
    Retrieve the top 5 only - or all if less than 5."""
    category_list = Category.objects.order_by('-likes')[:5]
    # order_by() with '-' yields order descending. the [:5] gives first five.
    """Place the list in our context_dict dictionary, which will be passed to the
    template engine."""
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')


def category(request, category_name_slug):
    # create a context dictionary which we can pass to the template
    context_dict = {}
    try:
        # look and see if there's a cat name w/this slug.
        # .get() with raise DoesNotExist if there isn't.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        # retreive all associated pages.
        # note that filter returns 1+ pages.
        pages = Page.objects.filter(category=category)
        # and then we add them to our context_dict dictionary.
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass  # we don't need to do this because it's handled in the template!
    return render(request, 'rango/category.html', context_dict)