from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "title" : "Главная страница",
        "title_page" : "Главная страница"
    }
    return render(request, "zayavki/index.html", context)

def zayavki(request):
    context = {
        "username" : "Нижний Новгород Мега",
        "role" : "магазин",
        "status" : "активный",
        "filters" : ["Все", "На рассмотрении", "На уценке", "Замена ценников", "Отклоненные", "Завершенные"],
        "title" : "Заявки на уценку",
        "title_page" : "Заявки на уценку"
    }
    return render(request, "zayavki/zayavki.html", context)    