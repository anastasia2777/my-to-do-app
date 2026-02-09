from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите название'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Введите описание'})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', )
        forbidden_words = ["ужас", "ненавижу", "отстой"]

        for word in forbidden_words:
            if word.lower() in title.lower():
                raise ValidationError(f"Нельзя использовать слово {word}, это слишком грубо")
        return title

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