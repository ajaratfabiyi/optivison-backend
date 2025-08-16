from django.contrib import admin
from .models import KYCSubmission


@admin.register(KYCSubmission)
class KYCSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'document_type',
        'status',
        'submitted_at',
        'reviewed_at',
    )
    list_filter = ('status', 'document_type', 'submitted_at', 'reviewed_at')
    search_fields = ('user__email', 'user__username')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'reviewed_at')

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'document_type',
                'document_front',
                'document_back',
                'selfie',
                'status',
                'rejection_reason',
            )
        }),
        ('Timestamps', {
            'fields': (
                'submitted_at',
                'reviewed_at',
            )
        }),
    )
