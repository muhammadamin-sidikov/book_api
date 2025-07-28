from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from .models import OrderItem, Order

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=self.request.user)

class OrderStatusViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="status")
    def update_status(self, request, pk):
        order = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response({'error': 'Yangi status yuborilmadi.'}, status=status.HTTP_400_BAD_REQUEST)

        if (new_status == 'paid' and not request.user.is_staff) or (order.status == 'paid' and not request.user.is_staff):
            return Response({'permissions error': 'faqat admin yangilay oladi'},
                            status=status.HTTP_403_FORBIDDEN)

        if order.status == new_status:
            return Response({'mesage': f'status allaqachon {new_status} qilingan'})

        if new_status == 'cancelled':
            for item in order.items.all():
                item.book.quantity += item.quantity
                item.book.save()

        order.status = new_status
        order.save()

        return Response({"detail": f"Order statusi '{new_status}' ga o'zgartirildi."})



