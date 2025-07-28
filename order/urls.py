from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderStatusViewSet

router = DefaultRouter()
router.register('items', OrderItemViewSet)
router.register(r'update', OrderStatusViewSet, basename='orders')
router.register('', OrderViewSet)

urlpatterns = router.urls