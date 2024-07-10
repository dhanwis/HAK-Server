from rest_framework import serializers
from .models import *
from productadmin.serializers import *

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='item.product.name', read_only=True)
    product_image = serializers.ImageField(source='item.color.images.first.image', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'product_name', 'product_image', 'quantity', 'total_price', 'user']

    def get_total_price(self, obj):
        return obj.total_price
    
class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product.name', read_only=True)
    product_image = serializers.ImageField(source='product.color.images.first.image', read_only=True)
    product_price = serializers.FloatField(source='product.discount_price', read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'product_name', 'product_image', 'product_price', 'created_at', 'product']

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        product_id = validated_data.get('product').id
        wishlist_item = WishList(user_id=user_id, product_id=product_id)
        wishlist_item.save()
        return wishlist_item


class CheckOutSerializer(serializers.ModelSerializer):
    ordered_items = serializers.SerializerMethodField()

    class Meta:
        model = CheckOut
        fields = [
            'id', 'order', 'first_name', 'last_name', 'email', 'address', 'mobile_no',
            'company_name', 'country', 'city', 'state', 'postal_code', 'ordered_items',
            'order_status'
        ]

    def get_ordered_items(self, instance):
        cart_item = instance.order
        ordered_item = {
            'product_name': cart_item.item.product.name,
            'quantity': cart_item.quantity,
            'total': cart_item.item.discount_price * cart_item.quantity  # Assuming 'discount_price' in ProductVariant model
        }
        return ordered_item


class ProductDisplaySerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'color', 'actual_price', 'discount_price', 'stock']

class ReviewSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Review
        fields = "__all__"