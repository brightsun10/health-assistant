# --- health_assistant/admin.py ---

from django.contrib import admin
from .models import HealthLog, ChatMessage

@admin.register(HealthLog)
class HealthLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'log_type', 'content', 'timestamp')
    list_filter = ('user', 'log_type', 'timestamp')
    search_fields = ('content',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'message')
    list_filter = ('user', 'timestamp')
    search_fields = ('message', 'response')

