# bridge/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),  # API endpoint
]
