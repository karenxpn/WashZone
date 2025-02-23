"""
URL configuration for WashZone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny

urlpatterns = [
       # path('admin/', admin.site.urls),
        path('api/v1/auth/', include('authentication.urls')),
        path('api/v1/', include('user.urls')),
        path('api/v1/', include('services.urls')),
        path('api/v1/', include('orders.urls')),
        path('silk/', include('silk.urls', namespace='silk')),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
