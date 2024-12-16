from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
