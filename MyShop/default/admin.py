from django.contrib import admin

from .models import Product, Basket, BasketItem, User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('price',)

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    ordering = ('-created_at',)

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')