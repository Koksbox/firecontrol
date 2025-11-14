from django.contrib import admin
from .models import FireObject, ObjectType
from .models import ResponsiblePerson

@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(FireObject)
class FireObjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'object_type', 'fire_class', 'is_archived']
    list_filter = ['object_type', 'fire_class', 'is_archived']
    search_fields = ['name', 'actual_address']


@admin.register(ResponsiblePerson)
class ResponsiblePersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'fire_object', 'email', 'assigned_at']
    list_filter = ['fire_object', 'assigned_at']
    search_fields = ['name', 'fire_object__name']