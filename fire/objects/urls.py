# objects/urls.py
from django.urls import path
from . import views

app_name = 'objects'

urlpatterns = [
    path('', views.object_list, name='list'),
    path('create/', views.object_create, name='create'),
    path('<int:pk>/', views.object_detail, name='detail'),
    path('<int:pk>/edit/', views.object_edit, name='edit'),
    path('<int:pk>/archive/', views.object_archive, name='archive'),
]