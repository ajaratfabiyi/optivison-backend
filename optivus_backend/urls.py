from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/kyc/', include('kyc.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/withdrawals/', include('withdrawals.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/admin-panel/', include('admin_panel.urls')),
    path('api/webhooks/', include('webhooks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
