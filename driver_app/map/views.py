
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.urls import reverse
from django.views import generic
from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from django.contrib.auth.models import User


# if user is signed in and has access to phone gps, show driver users on map if not driver
# if driver user is signed in, shows nothing on map until a non-driver requests a pickup
# if user is signed in but doesn't have location available, give option to look at map but not interact with users
# go to login page if not logged in
@login_required
def index(request):
    # set sessions
    user = request.user
    request.session['id'] = user.id
    info = user.userinfo_set.all().first()
    request.session['isdriver'] = info.is_driver
    # get all Users to display on the map
    info = User.objects.all()
    return render(request,"map/index.html", {'info': info})


# update the current users coordinates from the google map api
# updates every 40 seconds while on index
@login_required
def update_coords(request):
    # update coordinate values for the user by the cookie data
    curUser = get_object_or_404(User, pk=request.session['id'])
    curInfo = curUser.userinfo_set.all().first()
    # use default coordinates for abbotsford if nothing in cookie key
    curInfo.cur_lat = request.COOKIES.get('lat', '49.0504')
    curInfo.cur_long = request.COOKIES.get('long', '-122.285042')
    curInfo.save()
    # redirect back to index to show map
    return redirect(reverse('map:index'))


# sets the driver_id for the non-driver user that requests a pickup to the id of the driver they want
# uses this to display the users that want a pickup to the driver
@login_required
def book(request, user_id):
    # only allow if not driver
    if not request.session['isdriver']:
        # set the id for the driver that the user wants to be picked up by
        curUser = get_object_or_404(User, pk=request.session['id'])
        curInfo = curUser.userinfo_set.all().first()
        curInfo.driver_id = user_id
        curInfo.save()
        # set the session to track the driver to be booked to for use in user pickup completion
        request.session['driverid'] = user_id
    # redirect back to index to show map
    return redirect(reverse('map:index'))


# allows the requester to complete their pickup, resetting their driver_id for tracking the pickup driver to 0
# doing this removes them from the driver's map, indicating that their pickup is complete
@login_required
def complete(request):
    # reset the id for the driver that the user wants to be picked up by
    curUser = get_object_or_404(User, pk=request.session['id'])
    curInfo = curUser.userinfo_set.all().first()
    curInfo.driver_id = 0
    curInfo.save()
    # set the session to track the driver to be booked to 0
    request.session['driverid'] = 0
    # redirect back to index to show map
    return redirect(reverse('map:index'))


# displays the user profile depending on the user_id in the url
# also handles form posts from the profile page for users updating their information and other users submitting reviews on the page
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # get user info to send to template
    info = user.userinfo_set.all().first()

    # if form is posted, either update user information or create review
    if request.method == 'POST':
        # update database from update form
        if 'Update' in request.POST:
            # updates info only if something was entered in the field
            if request.POST.get("username") != "": user.username = request.POST.get("username")
            if request.POST.get("email") != "": user.email = request.POST.get("email")
            if request.POST.get("password1") != "": user.set_password(request.POST.get("password1"))
            if request.POST.get("bio") != "": info.bio = request.POST.get("bio")
            # save the uploaded profile pic file if a file is uploaded
            if len(request.FILES) != 0 and request.FILES['profpic'].size != 0:
                pic = request.FILES['profpic']
                info.image = pic
            # save both the changed user and info for that user
            user.save()
            info.save()
            # update session in case of password change
            update_session_auth_hash(request, user)

        # write new review from review form
        elif 'Review' in request.POST:
            # get the author for the review as the one issuing the request
            author = get_object_or_404(User, pk=request.session['id'])
            user.review_set.create(author=str(author), rating=request.POST.get('rating'), review_text=request.POST.get('revtext'))
            user.save()

        # go back to profile page after updates to it
        return HttpResponseRedirect(reverse('map:profile', args=(user.id,)))

    return render(request, 'map/profile.html', {'user': user, 'info': info})


# displays the register form on the register page and handles user creation on if form is posted
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # if the form is valid, use the information from it to create a new user and userinfo for that user
        if form.is_valid():
            email = form.cleaned_data['email']
            user_name = form.cleaned_data['user_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            is_driver = form.cleaned_data['is_driver']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            # create the userinfo for the newly created user
            uinfo = user.userinfo_set.create(is_driver=is_driver)
            # set image to default user image
            uinfo.image.name = 'no-img.jpg'
            uinfo.save()
            return HttpResponseRedirect(reverse('map:index'))
        # reshow form with errors if not valid
        else:
            errors = form.errors
            form = SignUpForm()
            return render(request, 'map/register.html', {'form': form, 'errors': errors})
    else:
        form = SignUpForm()
        return render(request, 'map/register.html', {'form': form})


# logs out of the current session and resets the user's driver_id to prevent from being tracked by drivers even on logout
def logout_view(request):
    # set the driver_id for the current user to 0 when logging off, so drivers dont keep users that never press compete pickup
    curUser = get_object_or_404(User, pk=request.session['id'])
    curInfo = curUser.userinfo_set.all().first()
    curInfo.driver_id = 0
    curInfo.save()

    logout(request)
    return redirect(reverse(settings.LOGIN_URL))


