from django.contrib import admin
from .models import KYCSubmission

@admin.register(KYCSubmission)
class KYCSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'document_type')
    search_fields = ('user__email',)
