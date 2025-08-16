from django.db import models
from django.conf import settings


class KYCSubmission(models.Model):
    DOCUMENT_TYPES = [
        ('passport', 'Passport'),
        ('driver_license', 'Driver License'),
        ('national_id', 'National ID'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='kyc_submission'
    )
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        blank=True,
        null=True
    )
    document_front = models.ImageField(
        upload_to='kyc/documents/front/',
        blank=True,
        null=True
    )
    document_back = models.ImageField(
        upload_to='kyc/documents/back/',
        blank=True,
        null=True
    )
    selfie = models.ImageField(
        upload_to='kyc/selfies/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.status}"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "KYC Submission"
        verbose_name_plural = "KYC Submissions"
