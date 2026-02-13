from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Task

FORBIDDEN_WORDS = ["ужас", "ненавижу", "отстой"]

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите название'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Введите описание'})
        }

    def _validate_forbidden_words(self, value, field_name):
        for word in FORBIDDEN_WORDS:
            if word.lower() in value.lower():
                raise ValidationError(f"Нельзя использовать слово «{word}» в поле «{field_name}», это слишком грубо")
        return value

    def clean_title(self):
        title = self.cleaned_data.get('title', )
        return self._validate_forbidden_words(title, 'название задачи')

    def clean_description(self):
        description = self.cleaned_data.get('description', )
        return self._validate_forbidden_words(description, 'описание')


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