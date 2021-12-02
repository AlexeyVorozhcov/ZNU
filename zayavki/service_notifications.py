from users.models import User

from .models import EventNotification, Notifications2, Zayavka


def get_notifications(user: User) -> list:
    """Получить все уведомления, где получатель = user
    Возвращает список словарей в формате: {"created": дата, "text": текст уведомлений, "zayavka_id": id заявки, 
    на которую будет ссылаться уведомление})"""
    
    notifications = Notifications2.objects.filter(
        recipient=user).order_by("-id")
    result = []
    for ntf in notifications:
        result.append(
            {"created": ntf.created, "text": ntf.text, "zayavka_id": ntf.zayavka.id})
    return result


class MakerNotification():
    """Класс для создания уведомлений"""

    def __init__(self, user: User, zayavka: Zayavka, event: EventNotification):
        self.user = user
        self.zayavka = zayavka
        self.event = event

    def _to_identify_the_recipient(self) -> User:
        """Возвращает получателя уведомления"""
        if self.user == self.zayavka.user:
            return self.zayavka.manager
        if self.user == self.zayavka.manager:
            return self.zayavka.user

    def _get_text_notification(self) -> str:
        """Возвращает текст уведмления в зависимости от события"""
        if self.event == EventNotification.CREATE_ZAYAVKA:
            return EventNotification.CREATE_ZAYAVKA.value.replace("#", str(self.user.shop)) + f" <{self.zayavka}>"
        elif self.event in [EventNotification.ADD_COMMENT, EventNotification.SET_STATUS1_TRUE, EventNotification.SET_STATUS2_TRUE, EventNotification.SET_STATUS3_TRUE]:
            return self.event.value + f" <{self.zayavka}> "
        else:
            return None

    def create_notification(self):
        """Создать уведомление"""
        new_notifications = Notifications2(
            zayavka=self.zayavka, text=self._get_text_notification())
        new_notifications.save()
        new_notifications.recipient.add(self._to_identify_the_recipient())
