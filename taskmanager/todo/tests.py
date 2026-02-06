from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from .models import Task

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_task_creation(self):
        task = Task.objects.create(
            user=self.user,
            title="Купить молоко",
            description="Срочно!"
        )

        self.assertEqual(task.title, "Купить молоко")
        self.assertEqual(task.user, self.user)
        self.assertEqual(str(task), "Купить молоко")

class TaskListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='Alice', password='12345')
        self.user2 = User.objects.create_user(username='Dani', password='12345')

        Task.objects.create(user=self.user1, title="Alice's Task 1")
        Task.objects.create(user=self.user1, title="Alice's Task 2")

        Task.objects.create(user=self.user2, title="Dani's Task 1")

    def test_list_show_only_own_tasks(self):
        self.client.login(username='Alice', password='12345')
        response = self.client.get(reverse('todo:task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice's Task 1", html=True)
        self.assertContains(response, "Alice's Task 2", html=True)
        self.assertNotContains(response, "Dani's Task 1", html=True)