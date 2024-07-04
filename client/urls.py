from django.urls import path
from .views import *

urlpatterns = [
    path('cart/<int:user_id>/', CartView.as_view(), name='cart-view'),
    path('cart/<int:user_id>/<int:item_id>/', CartView.as_view(), name='cart-item-view'),

    path('wishlist/<int:user_id>/', WishlistView.as_view(), name='wishlist-view'),
    path('wishlist/<int:user_id>/<int:item_id>/', WishlistView.as_view(), name='wishlist-item-view'),
    
    path('order/<int:user_id>/', CheckOutView.as_view(), name='order-list'),
]