# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'object-types', views.ObjectTypeViewSet, basename='objecttype')
router.register(r'objects', views.FireObjectViewSet, basename='fireobject')
router.register(r'responsibles', views.ResponsiblePersonViewSet, basename='responsible')
router.register(r'extinguishers', views.FireExtinguisherViewSet, basename='extinguisher')
router.register(r'inspections', views.InspectionReportViewSet, basename='inspection')
router.register(r'photos', views.InspectionPhotoViewSet, basename='inspectionphoto')
router.register(r'normative', views.NormativeDocumentViewSet, basename='normative')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('auth/token/', views.token_obtain_pair, name='token_obtain_pair'),
    path('auth/token-pin/', views.token_with_pin, name='token_with_pin'),
    path('auth/set-pin/', views.set_pin, name='set_pin'),
    path('push/register/', views.PushTokenView.as_view(), name='push_register'),

    path('sync/changes/', views.sync_changes, name='sync_changes'),
    path('sync/push/', views.sync_push_changes, name='sync_push_changes'),

    path('', include(router.urls)),
]
