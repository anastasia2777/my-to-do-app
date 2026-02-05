from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="tasks")
    title=models.CharField(max_length=200, verbose_name="Название задачи")
    description=models.TextField(blank=True, verbose_name="Описание задачи")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

