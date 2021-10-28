from django.shortcuts import render

# Create your views here.

def index(request):
    template = "main_page/index.html"
    context = {
        "title" : "Главная страница",
        "title_page" : "Главная страница"
    }
    return render(request, template, context)    