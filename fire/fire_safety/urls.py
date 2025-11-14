# fire_safety/urls.py
from django.urls import path
from . import views

app_name = 'fire_safety'

urlpatterns = [
    path('', views.extinguisher_list, name='list'),
    path('create/', views.extinguisher_create, name='create'),
    path('<int:pk>/', views.extinguisher_detail, name='detail'),
    path('<int:pk>/edit/', views.extinguisher_edit, name='edit'),
    path('<int:pk>/deactivate/', views.extinguisher_deactivate, name='deactivate'),
]