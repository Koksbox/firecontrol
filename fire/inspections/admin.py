# inspections/admin.py
from django.contrib import admin
from .models import InspectionReport, InspectionPhoto

class PhotoInline(admin.TabularInline):
    model = InspectionPhoto
    extra = 1

@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = ['fire_object', 'inspector', 'date', 'status']
    list_filter = ['status', 'date', 'inspector']
    inlines = [PhotoInline]

@admin.register(InspectionPhoto)
class InspectionPhotoAdmin(admin.ModelAdmin):
    list_display = ['inspection', 'caption']