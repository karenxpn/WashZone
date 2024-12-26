from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .service_views import category, provider, service, feature

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', category.CategoryViewSet, basename='category')
router.register(r'providers', provider.ProviderViewSet, basename='provider')
router.register(r'services', service.ServiceViewSet, basename='service')
router.register(r'features', feature.FeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
