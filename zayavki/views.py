from django.shortcuts import render
from zayavki.models import Zayavka
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    template = "zayavki/index.html"
    context = {
        "title" : "Главная страница",
        "title_page" : "Главная страница"
    }
    return render(request, template, context)

@login_required()
def page_view(request):
    template = "zayavki/page_view.html"
    context = {
        "username" : "Нижний Новгород Мега",
        "role" : "магазин",
        "status" : "активный",
        "filters" : ["Все", "Ждут рассмотрения", "Ждут уценки в 1С", "Ждут уценки на витрине", "Отклоненные", "Архивные"],
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


     