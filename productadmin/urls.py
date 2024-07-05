from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet),
router.register(r'products', ProductViewSet),
router.register(r'size',SizeViewSet),
router.register(r'ColorImage',ColorImageViewSet),
router.register(r'Color',ColorViewSet),
router.register(r'ProductVariant',ProductVariantViewSet),

urlpatterns = [
    path('', include(router.urls)),
]