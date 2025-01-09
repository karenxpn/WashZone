from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .service_views import category, provider, service, feature

router = DefaultRouter(trailing_slash=False)
router.register(r'api/v1/categories', category.CategoryViewSet, basename='category')
router.register(r'api/v1/providers', provider.ProviderViewSet, basename='provider')
router.register(r'api/v1/services', service.ServiceViewSet, basename='service')
router.register(r'api/v1/features', feature.FeatureViewSet, basename='feature')

urlpatterns = [
    path('', include(router.urls)),
]
