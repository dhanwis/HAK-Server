from django.urls import path
from .views import *
from rest_framework_simplejwt.views  import (
    TokenRefreshView,
)
urlpatterns=[ 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/',CustomerListCreate.as_view(),name='user-list-create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer/<int:customer_id>/verify-otp/',CustomerVerifyOTP.as_view(),name='user-verify-otp'),
    path('customer/<int:customer_id>/regenerate-otp/', CustomerRegenerateOTP.as_view(), name='user-regenerate-otp'),
    path('user/customer/profile/add/', UserProfileGetAdd.as_view()),
]