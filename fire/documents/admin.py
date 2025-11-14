# documents/admin.py
from django.contrib import admin
from .models import ObjectDocument

@admin.register(ObjectDocument)
class ObjectDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'doc_type', 'fire_object', 'valid_until', 'uploaded_by', 'uploaded_at']
    list_filter = ['doc_type', 'valid_until', 'uploaded_at']
    search_fields = ['title', 'fire_object__name']
    date_hierarchy = 'uploaded_at'