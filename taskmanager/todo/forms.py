from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите название'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Введите описание'})
        }
