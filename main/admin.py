from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email_field')
    list_filter = ('first_name', 'last_name', 'email_field')
    search_fields = ('first_name', 'last_name', 'email_field')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'order_id', 'order_date', 'complete')
    list_filter = ('order_date', 'complete')
    search_fields = ('order_id', 'order_date')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')
    list_filter = ('date_added', 'quantity')
    search_fields = ('date_added', 'quantity')


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('client', 'order', 'address', 'city', 'state', 'zipcode', 'date_added')
    list_filter = ('address', 'city', 'state', 'zipcode', 'date_added')
    search_fields = ('address', 'city', 'state', 'zipcode', 'date_added')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'commenter', 'date_created')
    list_filter = ('product', 'commenter', 'date_created')
    search_fields = ('product', 'commenter', 'date_created')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Shipping, ShippingAdmin)
