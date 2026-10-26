from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

# Customize Django Admin Header and Title for Professor's Vet Care
admin.site.site_header = "Professor's Vet & Pet Care Admin Panel"
admin.site.site_title = "Professor's Vet Care Admin"
admin.site.index_title = "Clinic & E-Commerce Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('gallery/', include('gallery.urls')),
    path('shop/', include('shop.urls')),
    
    # Production-ready media file serving for Cloud Platforms (Render, Railway, PythonAnywhere)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
