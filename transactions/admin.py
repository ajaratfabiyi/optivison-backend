from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tx_type', 'amount', 'status', 'created_at')
    search_fields = ('user__email', 'reference')
    list_filter = ('tx_type', 'status', 'created_at')
