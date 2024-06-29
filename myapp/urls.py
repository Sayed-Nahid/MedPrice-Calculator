from django.urls import path
from .views import *

urlpatterns = [
    path('capture/', capture_image, name='capture_image'),
    path('correct_class/<int:image_id>/', correct_class, name='correct_class'),
    # path('products/', product_list, name='product_list'),
    # path('products/<int:pk>/', product_detail, name='product_detail'),
    # path('products/new/', product_create, name='product_create'),
    # path('products/<int:pk>/edit/', product_update, name='product_update'),
    # path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    # path('get_cart_items/', get_cart_items, name='get_cart_items'),
    path('delete_cart_item/<int:id>/', delete_cart_item, name='delete_cart_item'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('inventory/', inventory, name='inventory'),
]
