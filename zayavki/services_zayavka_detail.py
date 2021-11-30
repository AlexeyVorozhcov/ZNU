from .models import Zayavka
from users.models import User




class ZayavkaProperties():
    def __init__(self, zayavka:Zayavka, user:User):
        self.zayavka = zayavka
        self.user = user
    
    def get_btns(self) -> list:
        """Возвращает данные о кнопках, которые должен отобразть шаблон
        Формат кнопки: {"btn_class": css-класс, "btn_value": Текст на кнопке, "btn_name": текстовая команда для контроллера}
        """
        btns = [] 
        if  self.is_can_be_edited():
            btns.append({"btn_class": "btn-primary", "btn_value":"Редактировать заявку", "btn_name":"_edit"})  
            btns.append({"btn_class": "btn-secondary", "btn_value":"Отправить в архив", "btn_name":"_status5"}) 
        if  self.is_can_be_approved():
            btns.append({"btn_class": "btn-success", "btn_value":"Заявку одобряю, новая цена назначена", "btn_name":"_status1"}) 
            btns.append({"btn_class": "btn-danger", "btn_value":"Отклонить заявку", "btn_name":"_status2"}) 
        if  self.is_can_be_cancel_approved():
            btns.append({"btn_class": "btn-warning", "btn_value":"Отменить решение", "btn_name":"_cancel_approve"})     
        if  self.is_can_be_discounted_in_1C():
            btns.append({"btn_class": "btn-success", "btn_value":"Уценка в 1С произведена", "btn_name":"_status3"}) 
        if  self.is_can_be_cancel_discounted_in_1C():
            btns.append({"btn_class": "btn-warning", "btn_value":"Отменить уценку в 1С", "btn_name":"_status3"})    
        if  self.is_can_be_discounted_in_shop():
            btns.append({"btn_class": "btn-success", "btn_value":"Товар на витрине уценен", "btn_name":"_status4"}) 
        if  self.is_can_be_cancel_discounted_in_shop():
            btns.append({"btn_class": "btn-warning", "btn_value":"Отменить уценку на витрине", "btn_name":"_status4"})     
        if  self.is_can_be_sent_to_archive():
            btns.append({"btn_class": "btn-secondary", "btn_value":"Отправить в архив", "btn_name":"_status5"}) 
        if  self.is_can_be_restored():
            btns.append({"btn_class": "btn-secondary", "btn_value":"Восстановить из архива", "btn_name":"_status5"}) 
        return btns      
    
    def is_can_be_edited(self)-> bool:
        # можно ли заявку редактировать
        if self.zayavka.user.shop == self.user.shop and not self.zayavka.status1 and not self.zayavka.status2 and not self.zayavka.status5:
            return True
        else:
            return False
        
    def is_can_be_approved (self)-> bool:
        # можно ли согласовывать
        if not self.zayavka.status1 and not self.zayavka.status2 and not self.zayavka.status5 and self.user.role.namerole[:3] == "Мен":
            return True
        else: 
            return False  
            
    def is_can_be_cancel_approved (self)-> bool:
        # можно ли согласовывать
        if (self.zayavka.status1 or self.zayavka.status2) and not self.zayavka.status3 and not self.zayavka.status5 and self.user.role.namerole[:3] == "Мен":
            return True
        else: 
            return False      
        
    def is_can_be_discounted_in_1C (self)-> bool:
        # можно ли уценять в 1С
        if self.zayavka.status1 and not self.zayavka.status3 and not self.zayavka.status5 and self.user.role.namerole == "Менеджер по уценке":
            return True
        else: 
            return False  

    def is_can_be_cancel_discounted_in_1C (self)-> bool:
        # можно ли уценять в 1С
        if self.zayavka.status3 and not self.zayavka.status4 and not self.zayavka.status5 and self.user.role.namerole == "Менеджер по уценке":
            return True
        else: 
            return False     
        
    def is_can_be_discounted_in_shop (self)-> bool:
        # можно ли уценять в магазине
        if self.zayavka.status3 and not self.zayavka.status4 and not self.zayavka.status5 and self.user.role.namerole == "Магазин":
            return True
        else: 
            return False  
        
    def is_can_be_cancel_discounted_in_shop (self) -> bool:
        # можно ли уценять в магазине
        if self.zayavka.status4 and not self.zayavka.status5 and self.user.role.namerole == "Магазин":
            return True
        else: 
            return False      
        
    def is_can_be_sent_to_archive (self) -> bool:
        # можно ли отправить в архив
        if (self.zayavka.status4 or self.zayavka.status2) and not self.zayavka.status5 and (self.user.role.namerole == "Магазин" or self.user.role.namerole == "Менеджер по уценке"):
            return True
        else: 
            return False      
        
    def is_can_be_restored (self)  -> bool:
        # можно ли восстановить из архива
        if self.zayavka.status5:
            return True
        else: 
            return False      
    def is_access_open(self) -> bool:
        """Возвращает bool -  доступна заявка пользователю или нет"""
        if self.zayavka.user.shop == self.user.shop or self.user.role.namerole[:3] == "Мен":
            return True
        else:
            return False
        
    def get_status_as_text(self) -> str:
        """Возвращает статус заявки в виде текста"""
        result = ""
        if self.zayavka.status4: result = "Одобрена, уценка в 1С - ОК, уценка на витрине - ОК"
        elif self.zayavka.status3: result = "Одобрена, уценка в 1С - ОК, ожидает уценки на витрине"
        elif self.zayavka.status2: result = "Отклонена"
        elif self.zayavka.status1: result = "Одобрена, ожидает уценки в 1С"  
        else: result = "На рассмотрении"
        if self.zayavka.status5: result += ". АРХИВНАЯ"
        return result    