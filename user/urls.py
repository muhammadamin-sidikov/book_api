from django.urls import path
from .views import RegisterAPIView, UserDetailView, LoginAPIView

urlpatterns = [
    path('users/', RegisterAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/login/', LoginAPIView.as_view(), name='user-login')
]