from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    price_per_item = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'book_title', 'quantity', 'price_per_item', 'total_price']

    def validate(self, data):
        book = data.get('book')
        quantity = data.get('quantity')

        if book.quantity < quantity:
            raise serializers.ValidationError(f"{book.title} kitobdan faqat {book.quantity} dona mavjud.")

        return data

    def create(self, validated_data):
        book = validated_data['book']
        quantity = validated_data['quantity']

        validated_data['price_per_item'] = book.price

        book.quantity -= quantity
        book.save()

        return super().create(validated_data)

    def get_total_price(self, obj):
        return float(obj.price_per_item) * obj.quantity

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='item', read_only=True)
    total_price = serializers.ReadOnlyField()
    sum_prices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'ordered_at', 'updated_at', 'total_price', 'sum_prices', 'items']
        read_only_fields = ['user', 'total_price', 'ordered_at', 'updated_at']

    def get_sum_prices(self, obj):
        return sum([i.total_price for i in obj.item.all()])


