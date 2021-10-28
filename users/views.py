from django.shortcuts import render

# Create your views here.


def index(request):
    template = "users/login.html"
    context = {
        "title": "Авторизация",
        "title_page": "Авторизация"
    }
    return render(request, template, context)
