from django.shortcuts import render
from zayavki.models import Zayavka

# Create your views here.

def index(request):
    template = "zayavki/index.html"
    context = {
        "title" : "Главная страница",
        "title_page" : "Главная страница"
    }
    return render(request, template, context)

def page_view(request):
    template = "zayavki/page_view.html"
    context = {
        "username" : "Нижний Новгород Мега",
        "role" : "магазин",
        "status" : "активный",
        "filters" : ["Все", "На рассмотрении", "Одобренные", "Отклоненные", "Уцененные", "Выполненные"],
        "title" : "Заявки на уценку",
        "title_page" : "Заявки на уценку",
        "data_from_model_Zayavka" : Zayavka.objects.all()
    }
    return render(request, template, context)   

def one_zayavka(request):
    id = 1
    template = "zayavki/one_zayavka.html"
    context = {
        "username" : "Нижний Новгород Мега",
        "role" : "магазин",
        "status" : "активный",
        "data_from_model_Zayavka" : Zayavka.objects.filter(id=id)
    }
    return render(request, template, context)    


     