from zayavki.models import Zayavka, FiltersOfZayavok

def get_data_from_model_Zayavka(filter_link, user):
    """Возвращает выборку из таблицы по условиям фильтра.  
       
    Если пользователь=Магазин - выборка записей этого магазина. 
    Если пользователь=Менеджер - выборка тех записей, категория которых есть в списке рабочих категорий менеджера.
    Далее выборка по статусам в зависимости от filter. 
    Сортировка по id

    Args:
        filter ([str]): [фильтр заявок]
        user ([AbstractBaseUser]): [пользователь]

    Returns:
        [QuerySet]: [список записей из базы данных]
    """ 
    new_queryset= None # первичная выборка базы для юзера (записи только для конкретного магазина или менеджера)
    # если Магазин, то отбираются все заявки с этим магазином
    if user.role.namerole == "Магазин":
        new_queryset = Zayavka.objects.filter(
            user__shop=user.shop).order_by("-id")
    else: # иначе отбираются те заявки, категории которых есть в списке рабочих категорий менеджера
        new_queryset = Zayavka.objects.filter(
            category__in=user.role.work_category.all()).order_by("-id")
    
    #Получить текущий фильтр для сравнения статусов заявок со статусами-шаблонами
    current_filter = FiltersOfZayavok.objects.get(link=filter_link)

    result = new_queryset.filter(
        status1__in=[True,False] if current_filter.status1==None else [current_filter.status1],
        status2__in=[True,False] if current_filter.status2==None else [current_filter.status2],
        status3__in=[True,False] if current_filter.status3==None else [current_filter.status3],
        status4__in=[True,False] if current_filter.status4==None else [current_filter.status4],
        status5__in=[True,False] if current_filter.status5==None else [current_filter.status5],
        status6__in=[True,False] if current_filter.status6==None else [current_filter.status6]
    )
    return result
