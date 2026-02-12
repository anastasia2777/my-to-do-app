from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from .forms import TaskForm, CustomUserCreationForm
from .forms import CustomAuthenticationForm
from .models import Task

@never_cache
def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = []
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'user': request.user,})



class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "✅ Задача добавлена!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "❌ Ошибка при добавлении задачи!")
        return response

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'todo/task_update.html'
    success_url = reverse_lazy('todo:task_list')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, '✏️ Задача обновлена!')
        return super().form_valid(form)
@login_required
def task_delete(request, pk):
    task=get_object_or_404(Task, pk=pk, user=request.user)
    if request.method=="POST":
        task.delete()
        messages.success(request, "🗑️ Задача удалена!")
        return redirect('todo:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task':task})

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('todo:task_list')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'todo/register.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request,  "🎉 Регистрация успешна! Вы вошли в систему.")
        return redirect(self.success_url)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('todo:task_list')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, "Вы успешно вышли из системы.")
        return response

