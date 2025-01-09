from django.urls import path
from .views import UserDetailView, PresignedURLView

urlpatterns = [
    path('api/v1/user', UserDetailView.as_view(), name='user-detail'),
    path('api/v1/user/presigned-url', PresignedURLView.as_view(), name='presigned-url'),
]