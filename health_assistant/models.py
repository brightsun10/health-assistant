# health_assistant/models.py

from django.db import models
from django.contrib.auth.models import User

class HealthLog(models.Model):
    """Stores a piece of health data logged by the user via the agent."""
    class LogType(models.TextChoices):
        MEAL = 'MEAL', 'Meal'
        SYMPTOM = 'SYMPTOM', 'Symptom'
        EXERCISE = 'EXERCISE', 'Exercise'
        UNKNOWN = 'UNKNOWN', 'Unknown'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_logs')
    log_type = models.CharField(max_length=10, choices=LogType.choices, default=LogType.UNKNOWN)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_log_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class ChatMessage(models.Model):
    """Stores a single message in a chat session."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
