from .models import Zayavka, Comments2

def get_comments(zayavka:Zayavka):    
    """Возвращает queryset из комментариев, у который object_id равен id заявки"""
    return Comments2.objects.filter(object_id=zayavka.id).order_by("created")