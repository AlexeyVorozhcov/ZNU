from django.shortcuts import render, get_object_or_404
from zayavki.models import Zayavka
from zayavki.forms import AddZayavkaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, DetailView


KOL_RECORDS_ON_PAGE = 10
DICT_OF_FILTERS = {
            "Все активные": "all",
            "Ждут рассмотрения": "resh",
            "Ждут уценки в 1С": "utc",
            "Ждут уценки на витрине": "utc_inshop",
            "Отклоненные": "otkl",
            "Архивные": "arch"}

class ZayavkaDetail(DetailView):
    model = Zayavka
    template_name = "zayavki/zayavka_detail.html"
    context_object_name = "zayavka"

class ZayavkaUpdate(UpdateView):
    model = Zayavka
    template_name = "zayavki/add_zayavka.html"
    form_class = AddZayavkaForm


@login_required()
def page_view(request):
    '''
    В GET-запросе могут прийти параметры page и/или filter. 
    '''
    template = "zayavki/page_view.html"  # шаблон страницы
    page = request.GET.get('page', None) # выдергиваем из запроса page; если его нет - None
    cur_filter = request.GET.get('filter', None) # выдергиваем из запроса filter; если его нет - None
    if not cur_filter:
        # если filter не передан, или передано несуществующее значение, устанавливается фильтр
        # по умолчанию в зависимости от роли пользователя
        cur_filter = get_default_filter(user=request.user)
    if not page:
        # если page не передан или передано некорректное значение,
        # устанавливается первая страница пагинатора
        # TODO добавить проверку на page=положительное число
        page = 1
    
    context = {
        "filters": DICT_OF_FILTERS,
        "cur_filter": cur_filter,
        "title": "Заявки на уценку",        
        "data_from_model_Zayavka": get_data_from_model_Zayavka(filter=cur_filter, user=request.user, page=page)
    }
    return render(request, template, context)


def get_default_filter(user):
    '''
    Возвращает стартовый фильтр. Если вход без фильтра, то устанавливается стартовый фильтр в зависимости от
    роли пользователя. Если это магазин - стартовый фильтр будет 'Ждет уценки на витрине', 
    если менеджер = 'Ждут рассмотрения'.
    Возвращает исходный фильтр, если он не пустой
    '''
    if user.role.namerole == "Магазин":
        return DICT_OF_FILTERS["Ждут уценки на витрине"]
    if user.role.namerole[:3] == "Мен":
        return DICT_OF_FILTERS["Ждут рассмотрения"]
    
def get_data_from_model_Zayavka(filter, user, page):
    '''
    Возвращает выборку из таблицы по условиям фильтра. Если пользователь Магазин - выборка записей этого магазина. 
    Если пользователь Менеджер - выборка тех записей, категория которых есть в списке рабочих категорий менеджера.
    Далее выборка по статусам в зависимости от фильтра.
    '''
    result = None  # возвращаемый результат
    # первичная выборка базы для юзера (записи только для конкретного магазина или менеджера)
    bd_for_user = None
    # если Магазин, то отбираются все заявки с этим магазином
    if user.role.namerole == "Магазин":
        bd_for_user = Zayavka.objects.filter(user__shop=user.shop).order_by("-data")
    else:
        bd_for_user = Zayavka.objects.filter(
            category__in=user.role.work_category.all()).order_by("-data")
    
    arch = bd_for_user.filter(status5=True)  # архивные
    all_z = bd_for_user.filter(status5=False)  # все кроме архивных
    resh = all_z.filter(status1=False, status2=False)  # ожидающие решения
    ok_resh = all_z.filter(status1=True)  # одобренные
    not_resh = all_z.filter(status2=True)  # отклоненные
    utc = ok_resh.filter(status3=False)  # ожидающие уценки в 1С
    ok_utc = ok_resh.filter(status3=True)  # уцененные в 1С
    utc_inshop = ok_utc.filter(status4=False)  # ожидающие уценки в магазине
    ok_utc_inshop = ok_utc.filter(status4=True)  # уцененные в магазине
    if not filter or filter == DICT_OF_FILTERS["Все активные"]:
        result = all_z
    if filter == DICT_OF_FILTERS["Ждут рассмотрения"]:
        result = resh
    if filter == DICT_OF_FILTERS["Архивные"]:
        result = arch
    if filter == DICT_OF_FILTERS["Отклоненные"]:
        result = not_resh
    if filter == DICT_OF_FILTERS["Ждут уценки в 1С"]:
        result = utc
    if filter == DICT_OF_FILTERS["Ждут уценки на витрине"]:
        result = utc_inshop
    paginator = Paginator(result, KOL_RECORDS_ON_PAGE)
    result_paginator = paginator.page(page)
    return result_paginator


@login_required
def add_zayavka(request):
    '''
    Просмотр(GET) или создание(POST) заявки.
    Трабл - программа не изменяет заявки, а создает новые со теми же полями, с новым id

    '''
    name_page = None    
    if request.method == "POST":
        form = AddZayavkaForm(data=request.POST, files=request.FILES, initial={'user': request.user})
        if form.is_valid(): 
            added_zayavka = form.save() 
            added_zayavka.user = request.user
            added_zayavka.save()
                       
        else:
            print (form.errors)
        return HttpResponseRedirect(reverse('zayavki:page_view'))
 
    form = AddZayavkaForm()    
    template = "zayavki/add_zayavka.html"
    context = {"form": form,
               "title": name_page,
               "name_page" : name_page}
    return render(request, template, context)
