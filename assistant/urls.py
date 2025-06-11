from rest_framework.routers import DefaultRouter
from django.urls import path, include

from assistant.views import AssistantQAView

router = DefaultRouter(trailing_slash=False)
router.register(r'ask', AssistantQAView, basename='ask')

urlpatterns = [
    path('', include(router.urls)),
]
