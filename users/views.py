from django.http.request import HttpHeaders
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm
from users.forms import UserRegistrationForm
from users.forms import UserProfileForm
# Create your views here.


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("main_page:index"))
    else:
        form = UserLoginForm()
    template = "users/login.html"
    context = {"form": form}
    return render(request, template, context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm
    template = "users/register.html"
    context = {"form": form}
    return render(request, template, context)


@login_required
def profile(request):
    if request.method=="POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        print(request.user.shop)
    template = "users/profile.html"
    context = {"form": form}
    # import pdb; pdb.set_trace()
    return render(request, template, context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main_page:index"))    
