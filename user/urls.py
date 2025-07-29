from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, UserDetailView, LoginAPIView, AuthorViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)

urlpatterns = [
    path('users/', RegisterAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/login/', LoginAPIView.as_view(), name='user-login')
]

urlpatterns += router.urls