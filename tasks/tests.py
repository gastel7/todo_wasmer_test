from django.test import TestCase
from django.urls import reverse

from .models import Task


class TodoTests(TestCase):
    def test_add_toggle_delete(self):
        self.client.post(reverse("index"), {"title": "Tester Wasmer"})
        task = Task.objects.get()
        self.assertFalse(task.done)

        self.client.post(reverse("toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.done)

        self.client.post(reverse("delete", args=[task.pk]))
        self.assertEqual(Task.objects.count(), 0)

    def test_health(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.json()["status"], "ok")
