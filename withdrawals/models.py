import uuid
from django.db import models
from django.conf import settings
from transactions.models import Transaction

class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='withdrawal_requests'
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='withdrawal_request',
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_paid(self):
        """Mark withdrawal as paid after service provider confirms."""
        if self.status != 'approved':
            raise ValueError("Withdrawal must be approved before marking as paid.")
        self.status = 'paid'
        self.save()

    def __str__(self):
        return f"Withdrawal {self.id} - {self.user.email} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['-requested_at']
        verbose_name = "Withdrawal Request"
        verbose_name_plural = "Withdrawal Requests"
