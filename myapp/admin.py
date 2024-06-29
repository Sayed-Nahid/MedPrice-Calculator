from django.contrib import admin
from .models import *
from django.apps import apps

# Register your models here.
@admin.register(ImageClassification)
class ImageClassificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'output_class', 'corrected_class', 'uploaded_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'quantity_in_stock', 'slug']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
