from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    """Query the database for a list of ALL categories
    Order the categories by number of likes in descending order.
    Retrieve the top 5 only - or all if less than 5."""
    category_list = Category.objects.order_by('-likes')[:5]
    # order_by() with '-' yields order descending. the [:5] gives first five.
    page_list = Page.objects.order_by('-views')[:5]
    """Place the list in our context_dict dictionary, which will be passed to the
    template engine."""
    context_dict = {'categories': category_list, 'popular_pages': page_list}

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
        context_dict['context_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    # is it a HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is the form valid?
        if form.is_valid():
            # save the new category
            form.save(commit=True)

            # call the index view & show the user the homepage
            return index(request)
        else:
            # if the form has errors, print them
            print(form.errors)
    else:
        # it's not a POST request, so display the form.
        form = CategoryForm()

    # bad form, bad form details, no form supplied...
    # render the form with error messages, if there are any.
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # if it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # attempt to grab info from raw form
        # we make use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # ... we save the form data to the db.
            user = user_form.save()

            # Now we hash the password using set_password method.
            # we update the user object once the pw is hashed
            user.set_password(user.password)
            user.save()

            # Now we work with the UserProfile instance.
            # We set the user attribute ourselves, so we set commit=False
            # so it won't save until we're ready to save
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did they provide a picture?
            # If they did we need to get it from the form and put it in the model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Registration is complete, so we change our registered variable to show this.
            registered = True
        # If the form isn't valid, info is missing, or there are mistakes, we show errors.
        else:
            print(user_form.errors, profile_form.errors)
    # if it's not POST we'll show our blank forms.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(request):

    # If the request if POST, try to pull relevant information.
    if request.method == 'POST':
        # get the username and password from the form
        username = request.POST['username']
        password = request.POST['password']

        # use django to see if the username/pw is valid. If it is, return User object
        user = authenticate(username=username, password=password)

        if user:
            # is the user active?
            if user.is_active:
                # login and redirect to homepage
                login(request, user)
                return HttpResponseRedirect('/rango/')
        else:
            # if the login credentials didn't pull up a User object
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # it's not a POST request, so display the login form
        return render(request, 'rango/login.html', {})
        # it's got a blank dictionary b/c there are no variable to pass to the template.


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")