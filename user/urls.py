from django.urls import path
from .views import UserDetailView, PresignedURLView

urlpatterns = [
    path('user', UserDetailView.as_view(), name='user-detail'),
    path('user/presigned-url', PresignedURLView.as_view(), name='presigned-url'),
]