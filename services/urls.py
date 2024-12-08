from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .service_views import category, provider, service, feature

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', category.CategoryViewSet)
router.register(r'providers', provider.ProviderViewSet)
router.register(r'services', service.ServiceViewSet)
router.register(r'features', feature.FeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
