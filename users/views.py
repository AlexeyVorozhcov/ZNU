from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

from users.forms import UserLoginForm

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
    context = {
        "title": "Авторизация",
        "form": form }
    return render(request, template, context)


def profile(request):
    template = "users/profile.html"
    context = {
        "title": "Профиль"}
    return render(request, template, context)


def register(request):
    template = "users/register.html"
    context = {
        "title": "Регистрация"}
    return render(request, template, context)
