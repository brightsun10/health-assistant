# --- health_agent_project/core/urls.py ---

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the urls from our health_assistant app
    path('', include('health_assistant.urls')),
    # Include Django's built-in auth URLs for login/logout
    path('accounts/', include('django.contrib.auth.urls')),
    # Redirect the root to our chat view for convenience
    path('', RedirectView.as_view(url='/chat/', permanent=False)),
]
