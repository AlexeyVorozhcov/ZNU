from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import resolve_url
from zayavki.models import Zayavka, Category

def get_gategories(qset:QuerySet):
        all = qset.objects.all()
        result = []
        for i, category in enumerate(all):
            result.append((str(i), category))
        return result    

class AddZayavkaForm(forms.ModelForm):
    name_class = "form-control py-4"
    attrs_for_code = {"class" : name_class,
                    'placeholder' : "Введите код товара"}
    attrs_for_name = {"class" : name_class,
                    'placeholder' : "Введите номенклатуру"}
    attrs_for_category = {"class" : name_class,
                    'placeholder' : "Выберите категорию"}
    attrs_for_description = {"class" : name_class,
                    'placeholder' : "Введите описание товарного вида"}
    attrs_for_clarification = {"class" : name_class,
                    'placeholder' : "Поясните причины и обстоятельства"}
    attrs_for_foto1 = {'placeholder' : "Добавьте фото №1"}                
    attrs_for_foto2 = {'placeholder' : "Добавьте фото №2"}

    code = forms.CharField(widget=forms.TextInput(attrs=attrs_for_code))
    name = forms.CharField(widget=forms.TextInput(attrs=attrs_for_name))
    category = forms.ChoiceField (widget=forms.RadioSelect, choices=get_gategories(Category))
    description = forms.CharField(widget=forms.Textarea(attrs=attrs_for_description))
    clarification = forms.CharField(widget=forms.Textarea(attrs=attrs_for_clarification))
    foto1 = forms.FileField(widget=forms.FileInput(attrs=attrs_for_foto1))
    foto2 = forms.FileField(widget=forms.FileInput(attrs=attrs_for_foto2))

    class Meta:
        model = Zayavka
        fields = ("code", "name", "category","description", "clarification", "foto1", "foto2")    

    