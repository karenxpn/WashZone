from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .slot_view import SlotView
from .views import OrderViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('slots', SlotView.as_view()),
]
