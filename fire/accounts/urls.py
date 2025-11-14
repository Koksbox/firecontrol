# accounts/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # login, logout и др.
]