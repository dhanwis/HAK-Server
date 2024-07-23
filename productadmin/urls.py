from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'size',SizeViewSet),


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category-detail'),
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    path('color-images/', ColorImageAPIView.as_view(), name='color-image-list'),
    path('color-images/<int:pk>/', ColorImageAPIView.as_view(), name='color-image-detail'),
    path('colors/', ColorAPIView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorAPIView.as_view(), name='color-detail'),
    path('product-variants/', ProductVariantAPIView.as_view(), name='product-variant-list'),
    path('product-variants/<int:pk>/', ProductVariantAPIView.as_view(), name='product-variant-detail'),
    path('customer-profiles/', CustomerProfilesAPIView.as_view(), name='customer-profiles'),
    path('allproducts/', AllProductViewAPIView.as_view(), name='allproductdisplay'),
    path('allproducts/<int:pk>/', AllProductViewAPIView.as_view(), name='allproductdisplay'),
    
    
    path('', include(router.urls)),
]