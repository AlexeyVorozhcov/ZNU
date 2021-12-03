from django.db.models.query import QuerySet
from .models import Zayavka, FiltersOfZayavok
from users.models import User
from .models import Notifications2

def get_users_default_filter(user:User) -> str:
    """Возвращает линк текущего фильтра пользователя по умолчанию, который зависит от роли пользователя"""        
    return FiltersOfZayavok.objects.get(for_roles=user.role).link

def get_users_queryset(user:User):
    """Возвращает пользовательский набор заявок без фильтра, т.е. всех заявок, которые доступны пользователю
    
    Если роль пользователя - Магазин, то отбираются все заявки, создателем которых является этот магазин
    Если роль пользователя - Менеджер, то отбираются те заявки, категории которых есть в рабочих категориях роли пользователя.
    """
    if user.role.namerole == "Магазин":
        return Zayavka.objects.filter(user__shop=user.shop).order_by("-id")
    else:
        return Zayavka.objects.filter(category__in=user.role.work_category.all()).order_by("-id")
    
def get_users_queryset_onfilter(user:User, filter_link:str):
    """ Возвращает queryset из пользовательского набора заявок с примененным фильтром filter_, отсортированных по убыванию id"""
    filter_ = FiltersOfZayavok.objects.get(link=filter_link)
    users_queryset = get_users_queryset(user)
    return users_queryset.filter(
            status1__in=[True,False] if filter_.status1==None else  [filter_.status1],
            status2__in=[True,False] if filter_.status2==None else  [filter_.status2],
            status3__in=[True,False] if filter_.status3==None else  [filter_.status3],
            status4__in=[True,False] if filter_.status4==None else  [filter_.status4],
            status5__in=[True,False] if filter_.status5==None else  [filter_.status5],
            status6__in=[True,False] if filter_.status6==None else  [filter_.status6]
            ).order_by("-id")    

def get_count_of_filter(user:User, filter_link:str):
    """Возвращает количество заявок по переданному фильтру у переданного юзера"""
    return get_users_queryset_onfilter(user, filter_link).count()

def get_listdict_of_filters_with_counts(user:User):
    """Возвращает список словарей в формате {"label":label, "link":link, "count":int}"""
    result = []
    for filter_ in FiltersOfZayavok.objects.all():
        temp = {"label":filter_.label, "link":filter_.link, "count":get_count_of_filter(user, filter_.link)}
        if temp["count"]==0: temp["count"] = "" 
        result.append(temp)    
    return result  
 



  

