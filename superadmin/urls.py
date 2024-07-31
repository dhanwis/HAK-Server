from django.urls import path
from .views import *

urlpatterns = [
    path('product-admin-profile/<int:pk>/', ProductAdminProfile.as_view(), name='product-admin-profile'),
    path("create/productadmin/",CreateProductAdminView.as_view(),name="create-productadmin"),
    path("create/orderadmin/", CreateOrderAdminView.as_view(), name="create-orderadmin"),
    path("order-admin-profile/<int:pk>", OrderAdminProfile.as_view(), name="order-admin-profile"),
    path("create/salesadmin/", CreateSalesAdminView.as_view(), name="create-salesadmin"),
    path("sales-admin-profile/<int:pk>", SalesAdminProfileView.as_view(), name="sales-admin-profile"),
    path("customre/deactivate-delete/<int:pk>/", DeactivateCustomerAPIView.as_view(), name="Deactivate-customer"),
    path('order-status-change/<int:pk>/', OrderStatusChangeAPIView.as_view(), name='order-status-change')
]
