from django.contrib import admin
from dropship.shop.models import ExtendedProfile, Order, OrderItem, Cart

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    readonly_fields = ('item', 'price', 'quantity', 'address', 'other_cost',
            'total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]

    readonly_fields = ('billing', 'total',)

admin.site.register(ExtendedProfile)
admin.site.register(Order, OrderAdmin)
