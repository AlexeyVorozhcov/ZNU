from comments.forms import CommentForm
from comments.models import Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
# from .utils import get_data_from_model_Zayavka, get_filters_for_template
from notifications.models import Notifications, create_notification
from users.models import User

from zayavki.forms import AddZayavkaForm
from zayavki.models import Zayavka
from .services_zayavka_list import get_users_queryset_onfilter, get_users_default_filter, get_listdict_of_filters_with_counts
from .services_zayavka_detail import ZayavkaProperties


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
            recipient_of_notification = User.objects.filter(role__namerole__startswith="Менеджер по уценке").get(role__work_category=zayavka.category)
            create_notification(recipient_of_notification, zayavka, "status1-true")        
        if '_status2' in request.POST:        
            zayavka.status1 = False
            zayavka.status2 = True
            recipient_of_notification =zayavka.user
            create_notification(recipient_of_notification, zayavka, "status2-true")                  
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
        context = super().get_context_data(**kwargs)
        zayavka = ZayavkaProperties(self.get_object(), self.request.user) 
        context["title"] = "Просмотр заявки"
        context["name_page"] = "Просмотр заявки"
        context["access_open"] = zayavka.is_access_open()         
        context["status_as_text"] = zayavka.get_status_as_text()               
        context['btns'] = zayavka.get_btns() 
        context['comments'] = self.get_comments()
        context['comments_form'] = CommentForm
     
        return context
    
    def get_comments(self):
        zayavka = self.get_object()
        return Comments.objects.filter(object_id=zayavka.id).order_by("created")
       

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
    
    def get_queryset(self):  
        """Возвращает пользовательский набор заявок на основании текущего фильтра и текущего пользователя"""    
        return get_users_queryset_onfilter(self.request.user, self.get_filter_from_post_or_default())
    
    def get_filter_from_post_or_default(self):
        """Возвращает параметр "filter" из полученного POST
        Если в POST нет параметра filter, возвращает фильтр текущего пользователя по умолчанию"""        
        return self.kwargs.get('filter', get_users_default_filter(self.request.user))
    
    
    def get_context_data(self, **kwargs):
        # заполняем контекст для передачи в шаблон
        context = super().get_context_data(**kwargs)
        context["title"] = "Заявки на уценку"
        context["name_page"] = "Заявки на уценку"
        context['filters'] = get_listdict_of_filters_with_counts(self.request.user)
        context['cur_filter'] = self.get_filter_from_post_or_default()   
        context['notifications'] = self.get_notifications()           
        return context
    
    def get_notifications(self):
        notifications = Notifications.objects.filter(recipient=self.request.user)
        result = []
        for ntf in notifications:
            result.append({"created":ntf.created, "text":ntf.text, "zayavka_id":ntf.zayavka.id})
        return result    
    
    
        
    
    
    
    




