# --- health_assistant/urls.py ---

from django.urls import path
from . import views

# This is necessary for namespacing if you have multiple apps
app_name = 'health_assistant'

urlpatterns = [
    # The main chat interface
    path('chat/', views.chat_view, name='chat'),
    # The endpoint for processing messages from the frontend
    path('process_message/', views.process_message, name='process_message'),
]
