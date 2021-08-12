from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static # new

urlpatterns = [
    path('vyom/', admin.site.urls),
    path('', include('shabd.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)