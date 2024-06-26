from django.urls import path
from .views import ProductAdminProfile,CreateProductAdminView

urlpatterns = [
    path('product-admin-profile/<int:pk>/', ProductAdminProfile.as_view(), name='product-admin-profile'),
    path("create/productadmin",CreateProductAdminView.as_view(),name="create-productadmin")
]
