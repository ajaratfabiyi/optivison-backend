from django.contrib import admin
from .models import WithdrawalRequest

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'requested_at')
    search_fields = ('user__email', 'account_number')
    list_filter = ('status', 'requested_at')
