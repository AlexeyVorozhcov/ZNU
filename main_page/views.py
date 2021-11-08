from django.shortcuts import render

# Create your views here.


def index(request):
    template = "main_page/index.html"
    context = {
        "title": "Главная страница"        
    }
    return render(request, template, context)

