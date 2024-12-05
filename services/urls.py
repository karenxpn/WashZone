from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .service_views import category

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', category.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
