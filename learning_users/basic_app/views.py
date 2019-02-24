from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Extra Import for the Login & Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")
# the above decorator is added tomake sure that the user is 
# logged in before viewing this special view

def register(request):

    registered = False

    if request.method == "POST":

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form directly to Database
            user = user_form.save()

            # Hash the password (goes to settings.py file and sets it as hash)
            user.set_password(user.password)

            # Update (saving changes to) the database with the Hashed password
            user.save()

            # EXTRA information

            # Can't commit (save to database) yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)
            # the above just prints out the actual errors
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.

    context = {
    'user_form': user_form,
    'profile_form': profile_form,
    'registered': registered
    }
    return render(request, 'basic_app/registration.html', context)



def user_login(request):

    if request.method == 'POST':
    # then the user have filled up the login information. First get the username and password supplied
    # grab them from the request.POST.get method, and get the name and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # below if we have a user (so passed the authentication process),
        # then check if the user is active, then log the user in

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user) # the login function we imported
                # take in the request, and the user object that was returned by authenticate
                # Send the user back to some page. (once they're logged in)
                # In this case their homepage, profile page or etc...
                # by using the HttpResponseRedirect to redirect them to some
                # other page (redirect them and call reverse on index)
                return HttpResponseRedirect(reverse('index'))
                # the above function will call redirect if they login and it's successful & 
                # their account is active, it will reverse them & redirect them back to the homepage
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # the request.method wasn't post, so they haven't
        # submitted anything, so just retrn the actual render of the page
        # Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})
        # above {} is just empty context dictionary

