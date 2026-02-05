from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите название'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Введите описание'})
        }
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label = 'Логин',
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label = 'Логин',
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}))
    password1 = forms.CharField(
        label = "Пароль",
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(
        label = "Пожтверждение пароля",
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']