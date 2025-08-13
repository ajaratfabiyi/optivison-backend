from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from .models import User, Referral


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'referred_by', 'referral_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Extra Info', {'fields': ('pin', 'is_kyc_verified', 'two_fa_enabled')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('email', 'username', 'is_staff', 'is_superuser', 'referred_by')
    search_fields = ('email', 'username')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        # If creating a user from admin and no referral provided, skip validation
        if not obj.is_staff and not obj.is_superuser and not obj.referred_by_id:
            # Option 1: Skip referral validation entirely
            obj.referred_by = None  # Admin-created normal user has no referral
            # Option 2 (optional): Auto-assign admin as referrer
            # obj.referred_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred', 'created_at')
    search_fields = ('referrer__email', 'referred__email')
    ordering = ('-created_at',)
