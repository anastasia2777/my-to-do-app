from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import TaskForm
from .models import Task


def task_list(request):
    tasks=Task.objects.all()
    return render(request, 'todo/task_list.html', {'tasks':tasks})

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✅ Задача добавлена!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "❌ Ошибка при добавлении задачи!")
        return response

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'todo/task_update.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        messages.success(self.request, '✏️ Задача обновлена!')
        return super().form_valid(form)

def task_delete(request, pk):
    task=get_object_or_404(Task, pk=pk)
    if request.method=="POST":
        task.delete()
        return redirect('todo:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task':task})

