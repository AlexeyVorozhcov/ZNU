from zayavki.models import Zayavka, FiltersOfZayavok

# def get_data_from_model_Zayavka(filter_, user):
#     """Возвращает выборку из таблицы по шаблону фильтра.  
       
#     Если пользователь=Магазин - выборка записей этого магазина. 
#     Если пользователь=Менеджер - выборка тех записей, категория которых есть в списке рабочих категорий менеджера.
#     Далее выборка по статусам в зависимости от filter_link. 
#     Сортировка по id

#     Args:
#         filter ([str]): [фильтр заявок]
#         user ([AbstractBaseUser]): [пользователь]

#     Returns:
#         [QuerySet]: [список записей из базы данных]
#     """ 
#     _users_queryset = _get_users_queryset(user)    
#     _filter = FiltersOfZayavok.objects.get(link=filter_)
#     return _get_list_zayavok_on_filter(_users_queryset, _filter)

# def _get_users_queryset(user):
#     # если роль пользователя = Магазин, то отбираются все заявки с этим магазином
#     if user.role.namerole == "Магазин":
#         return Zayavka.objects.filter(user__shop=user.shop).order_by("-id")
#     else: # иначе отбираются те заявки, категории которых есть в списке рабочих категорий менеджера
#         return Zayavka.objects.filter(category__in=user.role.work_category.all()).order_by("-id")

# def _get_list_zayavok_on_filter(_queryset, _filter):
#     return _queryset.filter(
#         status1__in=[True,False] if _filter.status1==None else  [_filter.status1],
#         status2__in=[True,False] if _filter.status2==None else  [_filter.status2],
#         status3__in=[True,False] if _filter.status3==None else  [_filter.status3],
#         status4__in=[True,False] if _filter.status4==None else  [_filter.status4],
#         status5__in=[True,False] if _filter.status5==None else  [_filter.status5],
#         status6__in=[True,False] if _filter.status6==None else  [_filter.status6]
#     ).order_by("-id")
    
# def _get_counts_of_filters(user):
#     """Возвращает словарь с количеством заявок в каждом фильтре в формате {"link" : int}"""
#     _users_queryset = _get_users_queryset(user)   
#     counts = {}
#     for _filter in FiltersOfZayavok.objects.all():
#         counts[_filter.link] = _get_list_zayavok_on_filter(_users_queryset, _filter).count()  
#         if counts[_filter.link]==0: counts[_filter.link] = ""     
#     return counts    

# def get_filters_for_template(user):
#     """Возвращает список словарей для использования в шаблоне в формате [{'label':label, 'link':link, 'count':count}]"""
#     result = []
#     counts = _get_counts_of_filters(user)
#     for filter_ in FiltersOfZayavok.objects.all():
#         result.append({"label":filter_.label, "link":filter_.link, "count":counts.get(filter_.link, "")})
#     return result    