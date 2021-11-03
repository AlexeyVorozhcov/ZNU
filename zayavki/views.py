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
def page_view(request, filter=None):
    template = "zayavki/page_view.html"
    context = {
        "username" : "Нижний Новгород Мега",
        "role" : "магазин",
        "status" : "активный",
        "filters" : {
            "Все" : "all", 
            "Ждут рассмотрения" : "resh",
            "Ждут уценки в 1С" : "utc", 
            "Ждут уценки на витрине" : "utc_inshop", 
            "Отклоненные" : "otkl", 
            "Архивные" : "arch"},
        "cur_filter" : filter,    
        "title" : "Заявки на уценку",
        "title_page" : "Заявки на уценку",
        "data_from_model_Zayavka" : get_data_from_model_Zayavka(filter=filter)
    }
    return render(request, template, context)   


def get_data_from_model_Zayavka(filter):
    '''
    Возвращает выборку из таблицы по условиям фильтра
    '''
    result = None
    if not filter or filter == "all": result = Zayavka.objects.all()
    if filter == "arch": result = Zayavka.objects.filter(status5__in=[True])  # архивные
    elif filter == "resh": result = Zayavka.objects.filter(status1__in=[False], status2__in=[False], status5__in=[False])  # ожидающие решения
    elif filter == "otkl": result = Zayavka.objects.filter(status1__in=[False], status2__in=[True], status5__in=[False])  # отклоненные
    elif filter == "utc": result = Zayavka.objects.filter(status1__in=[True],status3__in=[False], status5__in=[False])  # ожидающие уценки в 1с
    elif filter == "utc_inshop": result = Zayavka.objects.filter(status3__in=[True], status5__in=[False])  # ожидающие уценки в магазине

    return result

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


     