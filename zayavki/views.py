from django.shortcuts import render, get_object_or_404
from users.models import User
from zayavki.models import Zayavka, FiltersOfZayavok
from zayavki.forms import AddZayavkaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.models import Comments
from comments.forms import CommentForm
from .utils import get_data_from_model_Zayavka, get_filters_for_template
from notifications.models import create_notification, Notifications



KOL_RECORDS_ON_PAGE = 10



class ZayavkaCreate(LoginRequiredMixin, CreateView):

    model = Zayavka
    template_name = "zayavki/zayavka_create.html"
    form_class = AddZayavkaForm

    def form_valid(self, form):
        # Добавить текущего пользователя, кто создал заявку
        form.instance.user = self.request.user
        zayavka = form.save()
        # Определить получателя уведомления
        recipient_of_notification = User.objects.filter(role__namerole__startswith="Менеджер - ").get(role__work_category=zayavka.category)
        # Создать уведомление
        create_notification(recipient_of_notification, zayavka, "create")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Добавить данные в контекст, передаваемый в шаблон
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая заявка"
        context["name_page"] = "Новая заявка"
        return context

    def get_success_url(self):
        # Перенаправить после успешного создания заявки. TODO заменить на reverse_lazy, переадресацию на созданную заявку detail
        # zayavka = self.get_object()
        # create_notification(User.objects.get(role__work_category=zayavka.categoty), zayavka, "create")
        return reverse('zayavki:zayavki_list')

    

def process_command(request):
    """ Обработка нажатий кнопок в заявке"""
    if request.method=="POST":
        _id = request.POST['_id']
        zayavka = Zayavka.objects.get(id=_id)
        if '_edit' in request.POST:
            return HttpResponseRedirect(reverse('zayavki:zayavka-update', args=(_id,)))
        if '_status1' in request.POST:
            zayavka.status1 = True
            zayavka.status2 = False            
        if '_status2' in request.POST:        
            zayavka.status1 = False
            zayavka.status2 = True
        if '_cancel_approve' in request.POST:        
            zayavka.status1 = False
            zayavka.status2 = False
        if '_status3' in request.POST:
            zayavka.status3 = not zayavka.status3
        if '_status4' in request.POST:
            zayavka.status4 = not zayavka.status4
        if '_status5' in request.POST:
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
            for_btn.append({"btn_class": "btn-secondary", "btn_value":"Отправить в архив", "btn_name":"_status5"}) 
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
        context['comments'] = self.get_comments()
        context['comments_form'] = CommentForm
     
        return context
    
    def get_comments(self):
        zayavka = self.get_object()
        return Comments.objects.filter(object_id=zayavka.id).order_by("created")
        
        
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
        if zayavka.user.shop == self.request.user.shop and not zayavka.status1 and not zayavka.status2 and not zayavka.status5:
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
        # можно ли отправить в архив
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
        context['filters'] = get_filters_for_template(self.request.user)
        context['cur_filter'] = self.get_post_filter()   
        context['notifications'] = self.get_notifications()           
        return context
    
    def get_notifications(self):
        notifications = Notifications.objects.filter(recipient=self.request.user)
        result = []
        for ntf in notifications:
            result.append({"created":ntf.created, "text":ntf.text, "zayavka_id":ntf.zayavka.id})
        return result    
    
    def get_default_filter(self):
        """Получить текущий фильтр по умолчанию, который зависит от роли пользователя
                
        Returns:
            [str]: [значение поля link объекта из таблицы FiltersOfZayavok, в котором в поле for_roles есть роль текущего пользователя]
        """        
        result = FiltersOfZayavok.objects.get(for_roles=self.request.user.role).link
        return result
        
    def get_post_filter(self):
        """Получает параметр "filter" из полученного POST

        Returns:
            [str]: [значение в переданном параметре "filter" либо значение по умолчанию, полученное из метода self.get_default_filter]
        """        
        return self.kwargs.get('filter', self.get_default_filter())
    
    def get_queryset(self):  
        """Получает данные из БД на основании текущего фильтра заявок и текущего пользователя

        Returns:
            [QuerySet]: [список записей из базы данных]
        """        """"""    
        return get_data_from_model_Zayavka(self.get_post_filter(), self.request.user)
    




