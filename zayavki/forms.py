from typing import Dict
from django import forms

from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import resolve_url
from zayavki.models import Zayavka, Category
from users.models import User

def get_gategories(qset:QuerySet):
        all = qset.objects.all()
        result = []
        for i, category in enumerate(all):
            result.append((str(i), category))
        return result    




class AddZayavkaForm(forms.ModelForm):
    # id_user=0
    # def __init__(self, id_user, instance):
    #     super().__init__(self, instance)
    #     id_user = id_user

    name_class = "form-control form-control-sm fw-bold"
    attrs_for_code = {"class" : name_class,
                    'placeholder' : "Введите код товара",}
    attrs_for_name = {"class" : name_class,
                    'placeholder' : "Введите номенклатуру"}
    attrs_for_category = {"class" : name_class,
                    'placeholder' : "Выберите категорию"}
    attrs_for_description = {"class" : name_class, "style" : "height: 70px",
                    'placeholder' : "Введите описание товарного вида"}
    attrs_for_clarification = {"class" : name_class, "style" : "height: 70px",
                    'placeholder' : "Поясните причины и обстоятельства"}
    attrs_for_foto1 = {"class" : "form-control form-control-sm fw-bold",'placeholder' : "Добавьте фото №1"}                
    attrs_for_foto2 = {"class" : "form-control form-control-sm fw-bold",'placeholder' : "Добавьте фото №2"}
    
    
    code = forms.CharField(label="Код номенклатуры:", widget=forms.TextInput(attrs=attrs_for_code))
    name = forms.CharField(label="Наименование номенклатуры:",widget=forms.TextInput(attrs=attrs_for_name))
    category = forms.ModelChoiceField (Category.objects, label="Категория:",widget=forms.Select(attrs={"class":name_class}))
    description = forms.CharField(label="Описание товарного вида:",widget=forms.Textarea(attrs=attrs_for_description))
    clarification = forms.CharField(label="Пояснения:",widget=forms.Textarea(attrs=attrs_for_clarification))
    foto1 = forms.FileField(label="Приложите фото №1: ",widget=forms.FileInput(attrs=attrs_for_foto1), required=False)
    foto2 = forms.FileField(label="Приложите фото №2: ",widget=forms.FileInput(attrs=attrs_for_foto2), required=False)
    
    class Meta:
        model = Zayavka
        fields = ("code", "name", "category","description", "clarification", "foto1", "foto2")    

    # def set_user(self, new_user):
    #     data = self.data.copy()
    #     data['user'] = new_user
    #     self.data = data
           
        
    