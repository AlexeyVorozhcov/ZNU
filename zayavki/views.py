from django.shortcuts import render
from zayavki.models import Zayavka
from zayavki.forms import AddZayavkaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

KOL_RECORDS_ON_PAGE = 30


def index(request):
    template = "zayavki/index.html"
    context = {
        "title" : "Главная страница",
        "title_page" : "Главная страница"
    }
    return render(request, template, context)

@login_required()
def page_view(request):
    template = "zayavki/page_view.html" #шаблон страницы
    page = request.GET.get('page', None)
    filter_ = request.GET.get('filter', None)
    print(page)
    start_filter=filter_
    if not start_filter: 
        start_filter = get_start_filter(filter=start_filter, user=request.user)
    if not page:
        page=1
    context = {
        "filters" : {
            "Все активные" : "all", 
            "Ждут рассмотрения" : "resh",
            "Ждут уценки в 1С" : "utc", 
            "Ждут уценки на витрине" : "utc_inshop", 
            "Отклоненные" : "otkl", 
            "Архивные" : "arch"},
        "cur_filter" : start_filter,    
        "title" : "Заявки на уценку",
        "title_page" : "Заявки на уценку",
        "data_from_model_Zayavka" : get_data_from_model_Zayavka(filter=start_filter, user=request.user, page=page)
    }
    return render(request, template, context)   

def get_start_filter(filter, user):
    '''
    Возвращает стартовый фильтр. Если вход без фильтра, то устанавливается стартовый фильтр в зависимости от
    роли пользователя. Если это магазин - стартовый фильтр будет 'Ждет уценки на витрине', 
    если менеджер = 'Ждут рассмотрения'.
    Возвращает исходный фильтр, если он не пустой
    '''
    result = filter
    if not result:
        print(user.role.namerole[:3])
        if user.role.namerole == "Магазин": result="utc_inshop"
        if user.role.namerole[:3]=="Мен": result="resh"
    print ("Новый фильтр: ", filter)
    return result

def get_data_from_model_Zayavka(filter, user, page):
    '''
    Возвращает выборку из таблицы по условиям фильтра. Если пользователь Магазин - выборка записей, этого магазина. 
    Если пользователь Менеджер - выборка тех записей, категория которых есть в списке рабочих категорий менеджера.
    Далее выбора по статусам в зависимости от фильтра.
    '''
    result = None # возвращаемый результат
    bd_for_user = None # первичная выборка базы для юзера (записи только для конкретного магазина или менеджера)
    # если Магазин, то отбираются все заявки с этим магазином
    if user.role.namerole == "Магазин": bd_for_user = Zayavka.objects.filter(user__shop=user.shop)
    else:
        # print(user.role.work_category.all())
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
    paginator = Paginator(result, KOL_RECORDS_ON_PAGE)
    result_paginator = paginator.page(page)
    # print(result_paginator.paginator.num_pages )
    # print(result_paginator.object_list.get(id=1))
    return result_paginator

@login_required
def add_zayavka(request):
    if request.method=="POST":
        form = AddZayavkaForm(data=request.POST)
        if form.is_valid():
            new_zayavka = form.save()
            new_zayavka.user = request.user
            new_zayavka.save()
        else:
            pass #TODO вывести сообщение    
        return HttpResponseRedirect(reverse('zayavki:page_view'))
    else:
        idz = request.GET.get('idz', None)
        if idz: form = AddZayavkaForm(instance=Zayavka.objects.get(id=idz))
        else: form = AddZayavkaForm()
    
    template = "zayavki/add_zayavka.html"
    context = {"form": form}
    return render(request, template, context)  

    