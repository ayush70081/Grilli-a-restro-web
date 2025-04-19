from django.contrib import admin
from .models import (
    Reservation, 
    MenuItem, 
    # MenuItemOption,
    Order,
    OrderItem
)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

# @admin.register(MenuItemOption)
# class MenuItemOptionAdmin(admin.ModelAdmin):
#     list_display = ('menu_item', 'name', 'required')
#     list_filter = ('required',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_total')
    list_filter = ('order__status',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests')
    list_filter = ('date',)
    search_fields = ('name', 'phone')
