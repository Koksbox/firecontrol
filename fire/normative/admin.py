# normative/admin.py
from django.contrib import admin
from .models import NormativeDocument

@admin.register(NormativeDocument)
class NormativeDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'doc_number', 'issue_date']