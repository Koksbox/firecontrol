from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('objects/', include('objects.urls')),
    path('fire-safety/', include('fire_safety.urls')),
    path('dashboard/', include('core.urls')),
    path('documents/', include('documents.urls')),
    path('inspections/', include('inspections.urls')),
    path('normative/', include('normative.urls')),
    path('', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)