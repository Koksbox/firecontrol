# normative/urls.py
from django.urls import path
from . import views

app_name = 'normative'
urlpatterns = [
    path('', views.normative_list, name='list'),
]