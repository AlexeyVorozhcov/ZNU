from .forms import CommentForm
from .models import Comments2, EventNotification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
# from .utils import get_data_from_model_Zayavka, get_filters_for_template
from .models import Notifications2

from users.models import User

from zayavki.forms import AddZayavkaForm
from zayavki.models import Zayavka
from .services_zayavka_list import get_users_queryset_onfilter, get_users_default_filter, get_listdict_of_filters_with_counts
from .services_zayavka_detail import ZayavkaProperties
from .services_comments import get_comments
from .service_notifications import MakerNotification, get_notifications


KOL_RECORDS_ON_PAGE = 10

class ZayavkaFilterList(LoginRequiredMixin, ListView):
    '''Представление списка заявок'''
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
        context['notifications'] = get_notifications(self.request.user)
        return context


class ZayavkaCreate(LoginRequiredMixin, CreateView):

    model = Zayavka
    template_name = "zayavki/zayavka_create.html"
    form_class = AddZayavkaForm

    def form_valid(self, form):
        # Добавить текущего пользователя, кто создал заявку
        form.instance.user = self.request.user
        zayavka = form.save(commit=False)
        zayavka.manager = User.objects.filter(
            role__namerole__startswith="Менеджер - ").get(role__work_category=zayavka.category)
        zayavka.save()
        # Создать уведомление
        MakerNotification(self.request.user, zayavka, EventNotification.CREATE_ZAYAVKA).create_notification()
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
        zayavka = Zayavka.objects.get(id=_id)
        if '_edit' in request.POST:
            return HttpResponseRedirect(reverse('zayavki:zayavka-update', args=(_id,)))
        if '_status1' in request.POST:
            zayavka.status1 = True
            zayavka.status2 = False
            zayavka.manager = request.user
            MakerNotification(request.user, zayavka, EventNotification.SET_STATUS1_TRUE).create_notification()    
        if '_status2' in request.POST:        
            zayavka.status1 = False
            zayavka.status2 = True
            zayavka.manager = request.user
            MakerNotification(request.user, zayavka, EventNotification.SET_STATUS2_TRUE).create_notification()                  
        if '_cancel_approve' in request.POST:        
            zayavka.status1 = False
            zayavka.status2 = False
        if '_status3' in request.POST:
            zayavka.status3 = not zayavka.status3
            zayavka.manager = request.user
            MakerNotification(request.user, zayavka, EventNotification.SET_STATUS3_TRUE).create_notification()
        if '_status4' in request.POST:
            zayavka.status4 = not zayavka.status4
            zayavka.manager = request.user
        if '_status5' in request.POST:
            zayavka.status5 = not zayavka.status5
            zayavka.manager = request.user
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
        context['comments'] = get_comments(self.get_object())
        context['comments_form'] = CommentForm     
        return context
    
       

class ZayavkaUpdate(LoginRequiredMixin, UpdateView):
    model = Zayavka
    template_name = "zayavki/zayavka_create.html"
    form_class = AddZayavkaForm

    def form_valid(self, form):
        # Добавить текущего пользователя, кто создал заявку
        form.instance.user = self.request.user
        zayavka = form.save(commit=False)
        zayavka.manager = User.objects.filter(
            role__namerole__startswith="Менеджер - ").get(role__work_category=zayavka.category)
        zayavka.save()
        # Создать уведомление
        MakerNotification(self.request.user, zayavka, EventNotification.CREATE_ZAYAVKA).create_notification()
        return super().form_valid(form)


    
    
        
    
    
    
def add_comment(request):
    """ Обработка добавления комментария """       
    if request.method=="POST":
        _id = int(request.POST['_id'])    
        zayavka = Zayavka.objects.get(id=_id)      
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.autor = request.user
            comment.object_id = _id  
            comment.save()    
            MakerNotification(request.user, zayavka, EventNotification.ADD_COMMENT).create_notification()        
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
        else:
            print ("Что-то пошло не так.")
            print (form.data)
    else:
        return HttpResponseRedirect(reverse('zayavki:zayavki_list'))      




