from django.db import models


class Task(models.Model):
    title = models.CharField("titre", max_length=200)
    done = models.BooleanField("terminée", default=False)
    created_at = models.DateTimeField("créée le", auto_now_add=True)

    class Meta:
        ordering = ["done", "-created_at"]

    def __str__(self):
        return self.title
