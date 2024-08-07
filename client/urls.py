from django.urls import path,include
from .views import *

urlpatterns = [
    path('cart/<int:user_id>/', CartView.as_view(), name='cart-view'),
    path('cart/<int:user_id>/<int:item_id>/', CartView.as_view(), name='cart-item-view'),

    path('wishlist/<int:user_id>/', WishlistView.as_view(), name='wishlist-view'),
    path('wishlist/<int:user_id>/<int:item_id>/', WishlistView.as_view(), name='wishlist-item-view'),
                                     
    path('order/<int:user_id>/', CheckOutView.as_view(), name='order-list'),

    path('product/latest',LatestProductView.as_view(), name='product-latest'),
    path('product/bestseller',BestSellerView.as_view(), name='product-bestseller'),
    path('product/featured',FeaturedProductView.as_view(), name='product-featured'),
    path('product/trending',TrendingProductView.as_view(), name='product-trending'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/search/', ProductSearch.as_view(), name="product-search"),
    path('product/sort/', ProductSort.as_view(), name='product-sort'),
    path('product/review/<int:user_id>/', UserReview.as_view(), name='product-review'),
    path('product/<int:product_id>/review/', ProductReviewView.as_view(), name='review-product'),

    path('profile/<int:user_id>/',UserProfileUpdateView.as_view(), name='user-profile')
    
]