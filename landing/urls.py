from django.urls import path
from . import views
from django.contrib import admin


app_name = "landing"

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("join/", views.join_waitlist, name="join_waitlist"),
    path("try-ai-agent-step2/", views.try_ai_agent_step2, name="try_ai_agent_step2"),
    path('calling/', views.calling_page, name='calling_page'),
    path('admin/', admin.site.urls),
]
