# fire_safety/admin.py
from django.contrib import admin
from .models import FireExtinguisher

@admin.register(FireExtinguisher)
class FireExtinguisherAdmin(admin.ModelAdmin):
    list_display = ['inventory_number', 'type', 'fire_object', 'next_check_date', 'is_active']
    list_filter = ['type', 'is_active', 'next_check_date']
    search_fields = ['inventory_number', 'fire_object__name']
    date_hierarchy = 'next_check_date'