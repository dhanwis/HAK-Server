from django.urls import path
from .views import *
from rest_framework_simplejwt.views  import (
    TokenRefreshView,
)



urlpatterns=[ 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/',LoginView.as_view(),name='user-reg'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/<int:customer_id>/verify-otp/',CustomerVerifyOTP.as_view(),name='user-verify-otp'),
    path('customer/<int:customer_id>/regenerate-otp/', CustomerRegenerateOTP.as_view(), name='user-regenerate-otp'),
    path('customer/profile/add/', UserProfileAPIView.as_view(),name="userpro-add"),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/productadminview/', AllProductAdminView.as_view(), name="productadminview"),
]