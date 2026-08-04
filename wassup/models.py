from django.db import models

from django.db import models


class Message(models.Model):
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message}"