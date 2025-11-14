# inspections/urls.py
from django.urls import path
from . import views

app_name = 'inspections'

urlpatterns = [
    path('', views.inspection_list, name='list'),
    path('create/', views.inspection_create, name='create'),
    path('<int:pk>/', views.inspection_detail, name='detail'),
    path('<int:pk>/complete/', views.inspection_complete, name='complete'),
]