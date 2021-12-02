from .models import Notifications2, Zayavka, EventNotification
from users.models import User

def get_notifications(user:User):
        notifications = Notifications2.objects.filter(
            recipient=user).order_by("-id")
        result = []
        for ntf in notifications:
            result.append(
                {"created": ntf.created, "text": ntf.text, "zayavka_id": ntf.zayavka.id})
        return result  


class MakerNotification():
    """Класс для создания уведомлений
    
    Event:
    - create-zayavka - создание новой заявки
    - add-comment - добавление нового комментария
    - set-status1-true - одобрение заявки менеджеров
    - set-status2-true - отклонение заявки менеджером
    - set-status3-true - уценка в базе произведена
    - set-status4-true - уценка в магазине произведена
    - set-status5-true - заявка отправлена в архив    
    """
    def __init__(self, user:User, zayavka:Zayavka, event:EventNotification):
        self.user = user
        self.zayavka = zayavka
        self.event = event
        
    def _to_identify_the_recipient(self):
        """Возвращает получателя уведомления"""
        if self.user==self.zayavka.user:
            return self.zayavka.manager
        if self.user==self.zayavka.manager:
            return self.zayavka.user
        
    def _get_text_notification(self):
        """Возвращает текст уведмления в зависимости от события"""
        if self.event == EventNotification.CREATE_ZAYAVKA:
            return EventNotification.CREATE_ZAYAVKA.value.replace("#", str(self.user.shop)) + f" <{self.zayavka}>"
        elif self.event in [EventNotification.ADD_COMMENT, EventNotification.SET_STATUS1_TRUE, EventNotification.SET_STATUS2_TRUE, EventNotification.SET_STATUS3_TRUE]:
            return self.event.value + f" <{self.zayavka}> "
        else:
            return None
        
    def create_notification(self):
        new_notifications = Notifications2(zayavka=self.zayavka, text=self._get_text_notification())
        new_notifications.save()
        new_notifications.recipient.add(self._to_identify_the_recipient())    

               
                
                


# def create_notification(recipient, zayavka, type_):
#     text=""
#     if type_=="create":
#         text = f'Магазин {zayavka.user.shop} создал новую заявку на уценку товара "{zayavka.name}".'
#     if type_=="status1-true":
#         text = f'Менеджер одобрил заявку на уценку товара "{zayavka.name}".'    
#     if type_=="status2-true":
#         text = f'Менеджер отклонил вашу заявку на уценку товара "{zayavka.name}".'         
#     new_notifications = Notifications2(zayavka=zayavka, text=text)
#     new_notifications.save()
#     new_notifications.recipient.add(recipient)