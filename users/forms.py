from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class UserLoginForm(AuthenticationForm):
    name_class = 'form-control py-4'
    attrs_username = {"class" : name_class,
                    'placeholder' : "Введите имя пользователя"}
    attrs_password = {"class" : name_class,
                    'placeholder' : "Введите пароль"}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs_username))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_password))
    class Meta:
        model = User
        fields = ("username", "password")

class UserRegistrationForm (UserCreationForm):
    name_class = "form-control py-4"
    attrs_for_firstname = {"class" : name_class,
                    'placeholder' : "Введите имя"}
    attrs_for_last_name = {"class" : name_class,
                    'placeholder' : "Введите фамилию"}
    attrs_for_username = {"class" : name_class,
                    'placeholder' : "Введите имя пользователя"}
    attrs_for_email = {"class" : name_class,
                    'placeholder' : "Введите адрес эл. почты"}
    attrs_for_password1 = {"class" : name_class,
                    'placeholder' : "Введите пароль"}
    attrs_for_password2 = {"class" : name_class,
                    'placeholder' : "Подтвердите пароль"}

    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs_for_firstname))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs_for_last_name))
    username = forms.CharField(widget=forms.TextInput(attrs=attrs_for_username))
    email = forms.CharField(widget=forms.EmailInput(attrs=attrs_for_email))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_for_password1))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_for_password2))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")