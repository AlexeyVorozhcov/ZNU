from django.shortcuts import render, get_object_or_404
from zayavki.models import Zayavka
from zayavki.forms import AddZayavkaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


KOL_RECORDS_ON_PAGE = 8
DICT_OF_FILTERS = {
    "Все активные": "all",
    "Ждут рассмотрения": "resh",
    "Ждут уценки в 1С": "utc",
    "Ждут уценки на витрине": "utc_inshop",
    "Уцененные" : "ok_utc_inshop",
    "Отклоненные": "otkl",
    "Архивные": "arch"}


class ZayavkaCreate(LoginRequiredMixin, CreateView):

    model = Zayavka
    template_name = "zayavki/zayavka_create.html"
    form_class = AddZayavkaForm

    def form_valid(self, form):
        # Добавить текущего пользователя, кто создал заявку
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Добавить данные в контекст, передаваемый в шаблон
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая заявка"
        context["name_page"] = "Новая заявка"
        return context

    def get_success_url(self):
        # Перенаправить после успешного создания заявки. TODO заменить на reverse_lazy, переадресацию на созданную заявку detail
        return reverse('zayavki:zayavki_list')


def process_command(request):
    """ Обработка нажатий кнопок в заявке"""
    if request.method=="POST":
        _id = request.POST['_id']
        if '_edit' in request.POST:
            print ("Кнопка редактировать заявку ", _id)
            return HttpResponseRedirect(reverse('zayavki:zayavka-update', args=(_id,)))
        if '_status1' in request.POST:
            print ("Кнопка согласовано ", _id)
            zayavka = Zayavka.objects.get(id=_id)
            zayavka.status1 = True
            zayavka.status2 = False
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        if '_status2' in request.POST:
            print ("Кнопка отклонить ", _id)
            zayavka = Zayavka.objects.get(id=_id)            
            zayavka.status1 = False
            zayavka.status2 = True
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        if '_cancel_approve' in request.POST:
            print ("Кнопка отменить решение ", _id)
            zayavka = Zayavka.objects.get(id=_id)            
            zayavka.status1 = False
            zayavka.status2 = False
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        if '_status3' in request.POST:
            print ("Кнопка уценка в 1с ", _id)
            zayavka = Zayavka.objects.get(id=_id)
            zayavka.status3 = not zayavka.status3
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        if '_status4' in request.POST:
            print ("Кнопка уценка в магазине ", _id)
            zayavka = Zayavka.objects.get(id=_id)
            zayavka.status4 = not zayavka.status4
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        if '_status5' in request.POST:
            print ("Кнопка архив ", _id)
            zayavka = Zayavka.objects.get(id=_id)
            zayavka.status5 = not zayavka.status5
            zayavka.save()
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))


class ZayavkaDetail(LoginRequiredMixin, DetailView):
    model = Zayavka
    template_name = "zayavki/zayavka_detail.html"

     
    def get_context_data(self, **kwargs):
        # Добавить данные в контекст, передаваемый в шаблон
        context = super().get_context_data(**kwargs)
        context["title"] = "Просмотр заявки"
        context["name_page"] = "Просмотр заявки"
        context["access_open"] = self.is_access_open()         
        context["status_as_text"] = self.get_status_as_text()   
        for_btn = [] 
        if  self.is_can_be_edited():
            for_btn.append({"btn_class": "btn-primary", "btn_value":"Редактировать заявку", "btn_name":"_edit"})   
        if  self.is_can_be_approved():
            for_btn.append({"btn_class": "btn-success", "btn_value":"Заявку одобряю, новая цена назначена", "btn_name":"_status1"}) 
            for_btn.append({"btn_class": "btn-danger", "btn_value":"Отклонить заявку", "btn_name":"_status2"}) 
        if  self.is_can_be_cancel_approved():
            for_btn.append({"btn_class": "btn-warning", "btn_value":"Отменить решение", "btn_name":"_cancel_approve"})     
        if  self.is_can_be_discounted_in_1C():
            for_btn.append({"btn_class": "btn-success", "btn_value":"Уценка в 1С произведена", "btn_name":"_status3"}) 
        if  self.is_can_be_cancel_discounted_in_1C():
            for_btn.append({"btn_class": "btn-warning", "btn_value":"Отменить уценку в 1С", "btn_name":"_status3"})    
        if  self.is_can_be_discounted_in_shop():
            for_btn.append({"btn_class": "btn-success", "btn_value":"Товар на витрине уценен", "btn_name":"_status4"}) 
        if  self.is_can_be_cancel_discounted_in_shop():
            for_btn.append({"btn_class": "btn-warning", "btn_value":"Отменить уценку на витрине", "btn_name":"_status4"})     
        if  self.is_can_be_sent_to_archive():
            for_btn.append({"btn_class": "btn-secondary", "btn_value":"Отправить в архив", "btn_name":"_status5"}) 
        if  self.is_can_be_restored():
            for_btn.append({"btn_class": "btn-secondary", "btn_value":"Восстановить из архива", "btn_name":"_status5"})   
        context['btns'] = for_btn 
     
        return context
    
    def is_access_open(self):
        # открывать или нет заявку текущему пользователю
        if self.get_object().user.shop == self.request.user.shop or self.request.user.role.namerole[:3] == "Мен":
            return True
        else:
            return False
        
    def get_status_as_text(self):
        # получить статус заявки в виде текста
        zayavka = self.get_object()
        result = ""
        if zayavka.status4: result = "Одобрена, уценка в 1С - ОК, уценка на витрине - ОК"
        elif zayavka.status3: result = "Одобрена, уценка в 1С - ОК, ожидает уценки на витрине"
        elif zayavka.status2: result = "Отклонена"
        elif zayavka.status1: result = "Одобрена, ожидает уценки в 1С"  
        else: result = "На рассмотрении"
        if zayavka.status5: result += ". АРХИВНАЯ"
        return result
    
    def is_can_be_edited(self):
        # можно ли заявку редактировать
        zayavka = self.get_object()
        if zayavka.user.shop == self.request.user.shop and not zayavka.status1 and not zayavka.status2:
            return True
        else:
            return False
        
    def is_can_be_approved (self):
        # можно ли согласовывать
        zayavka = self.get_object()
        if not zayavka.status1 and not zayavka.status2 and not zayavka.status5 and self.request.user.role.namerole[:3] == "Мен":
            return True
        else: 
            return False  
         
    def is_can_be_cancel_approved (self):
        # можно ли согласовывать
        zayavka = self.get_object()
        if (zayavka.status1 or zayavka.status2) and not zayavka.status3 and not zayavka.status5 and self.request.user.role.namerole[:3] == "Мен":
            return True
        else: 
            return False      
        
    def is_can_be_discounted_in_1C (self):
        # можно ли уценять в 1С
        zayavka = self.get_object()
        if zayavka.status1 and not zayavka.status3 and not zayavka.status5 and self.request.user.role.namerole == "Менеджер по уценке":
            return True
        else: 
            return False  
    
    def is_can_be_cancel_discounted_in_1C (self):
        # можно ли уценять в 1С
        zayavka = self.get_object()
        if zayavka.status3 and not zayavka.status4 and not zayavka.status5 and self.request.user.role.namerole == "Менеджер по уценке":
            return True
        else: 
            return False     
        
    def is_can_be_discounted_in_shop (self):
        # можно ли уценять в магазине
        zayavka = self.get_object()
        if zayavka.status3 and not zayavka.status4 and not zayavka.status5 and self.request.user.role.namerole == "Магазин":
            return True
        else: 
            return False  
        
    def is_can_be_cancel_discounted_in_shop (self):
        # можно ли уценять в магазине
        zayavka = self.get_object()
        if zayavka.status4 and not zayavka.status5 and self.request.user.role.namerole == "Магазин":
            return True
        else: 
            return False      
        
    def is_can_be_sent_to_archive (self):
        # можно ли уценять в магазине
        zayavka = self.get_object()
        if (zayavka.status4 or zayavka.status2) and not zayavka.status5 and (self.request.user.role.namerole == "Магазин" or self.request.user.role.namerole == "Менеджер по уценке"):
            return True
        else: 
            return False      
        
    def is_can_be_restored (self):
        # можно ли восстановить из архива
        zayavka = self.get_object()
        if zayavka.status5:
            return True
        else: 
            return False      
                  

class ZayavkaUpdate(LoginRequiredMixin, UpdateView):
    model = Zayavka
    template_name = "zayavki/zayavka_create.html"
    form_class = AddZayavkaForm


class ZayavkaFilterList(LoginRequiredMixin, ListView):
    ''' 
    Представление списка заявок.
    '''
    model = Zayavka
    paginate_by = KOL_RECORDS_ON_PAGE
    template_name = "zayavki/zayavka_list.html"
    context_object_name = "zayavki"

    def get_context_data(self, **kwargs):
        # заполняем контекст для передачи в шаблон
        context = super().get_context_data(**kwargs)
        context["title"] = "Заявки на уценку"
        context["name_page"] = "Заявки на уценку"
        context['filters'] = DICT_OF_FILTERS
        context['cur_filter'] = self.get_post_filter()
        return context
    
    def get_default_filter(self):
        # получить фильтр по умолчанию, который зависит от роли пользователя
        if self.request.user.role.namerole == "Магазин":
            return DICT_OF_FILTERS["Ждут уценки на витрине"]
        elif self.request.user.role.namerole[:3] == "Мен":
            return DICT_OF_FILTERS["Ждут рассмотрения"]
        else:
            return DICT_OF_FILTERS["Все активные"]
        
    def get_post_filter(self):
        # получить фильтр из post
        return self.kwargs.get('filter', self.get_default_filter())
    
    def get_queryset(self):  
        # получить выборку из таблицы      
        return get_data_from_model_Zayavka(self.get_post_filter(), self.request.user)


def get_data_from_model_Zayavka(filter, user):
    '''
    Возвращает выборку из таблицы по условиям фильтра. Если пользователь Магазин - выборка записей этого магазина. 
    Если пользователь Менеджер - выборка тех записей, категория которых есть в списке рабочих категорий менеджера.
    Далее выборка по статусам в зависимости от фильтра. Сортировка по id
    '''
    result = None  # возвращаемый результат    
    bd_for_user = None # первичная выборка базы для юзера (записи только для конкретного магазина или менеджера)
    # если Магазин, то отбираются все заявки с этим магазином
    if user.role.namerole == "Магазин":
        bd_for_user = Zayavka.objects.filter(user__shop=user.shop).order_by("-id")
    else:
        bd_for_user = Zayavka.objects.filter(category__in=user.role.work_category.all()).order_by("-id")

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
    if filter == DICT_OF_FILTERS["Уцененные"]:
        result = ok_utc_inshop   
    return result


