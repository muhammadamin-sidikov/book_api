from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'ordered_at', 'updated_at', 'total_price')
    list_filter = ('status', 'ordered_at')
    search_fields = ('user__email',)
    inlines = [OrderItemInline]
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)