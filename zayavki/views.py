from django.shortcuts import render
from zayavki.models import Zayavka
from zayavki.forms import AddZayavkaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


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
        "filters" : {
            "Все активные" : "all", 
            "Ждут рассмотрения" : "resh",
            "Ждут уценки в 1С" : "utc", 
            "Ждут уценки на витрине" : "utc_inshop", 
            "Отклоненные" : "otkl", 
            "Архивные" : "arch"},
        "cur_filter" : filter,    
        "title" : "Заявки на уценку",
        "title_page" : "Заявки на уценку",
        "data_from_model_Zayavka" : get_data_from_model_Zayavka(filter=filter, user=request.user)
    }
    return render(request, template, context)   


def get_data_from_model_Zayavka(filter, user):
    '''
    Возвращает выборку из таблицы по условиям фильтра
    '''
    result = None # возвращаемый результат
    bd_for_user = None # первичная выборка базы для юзера (записи только для конкретного магазина или менеджера)
    # если Магазин, то отбираются все заявки с этим магазином
    if user.role.namerole == "Магазин": bd_for_user = Zayavka.objects.filter(user__shop=user.shop)
    else:
        print(user.role.work_category.all())
        bd_for_user = Zayavka.objects.filter(category__in=user.role.work_category.all())
    arch = bd_for_user.filter(status5=True) # архивные
    all = bd_for_user.filter(status5=False) # все кроме архивных
    resh = all.filter(status1=False, status2=False) # ожидающие решения
    ok_resh = all.filter(status1=True) # одобренные
    not_resh = all.filter(status2=True) # отклоненные
    utc = ok_resh.filter(status3=False) # ожидающие уценки в 1С
    ok_utc = ok_resh.filter(status3=True) # уцененные в 1С
    utc_inshop = ok_utc.filter(status4=False) # ожидающие уценки в магазине
    ok_utc_inshop = ok_utc.filter(status4=True) # уцененные в магазине
    if not filter or filter == "all": result = all
    if filter=="resh": result = resh
    if filter == "arch": result = arch
    if filter == "otkl": result = not_resh
    if filter == "utc": result = utc
    if filter == "utc_inshop": result = utc_inshop

    # if not filter or filter == "all": result = Zayavka.objects.all() # все
    # if filter=="resh": result = result.filter(status1=False, status2=False) # ожидающие решения
    # if filter == "arch": result = Zayavka.objects.filter(status5__in=[True])  # архивные
    # elif filter == "resh": result = Zayavka.objects.filter(status1__in=[False], status2__in=[False], status5__in=[False])  # ожидающие решения
    # elif filter == "otkl": result = Zayavka.objects.filter(status1__in=[False], status2__in=[True], status5__in=[False])  # отклоненные
    # elif filter == "utc": result = Zayavka.objects.filter(status1__in=[True],status3__in=[False], status5__in=[False])  # ожидающие уценки в 1с
    # elif filter == "utc_inshop": result = Zayavka.objects.filter(status3__in=[True], status5__in=[False])  # ожидающие уценки в магазине

    return result

@login_required
def add_zayavka(request):
    if request.method=="POST":
        form = AddZayavkaForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = AddZayavkaForm()
        print(request.user.shop)
    template = "zayavka/add_zayavka.html"
    context = {"form": form}
    # import pdb; pdb.set_trace()
    return render(request, template, context)  


     