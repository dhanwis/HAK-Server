from django.shortcuts import render
from rest_framework.views import APIView
from auth_app.serializers import UserProfileSerializer
from auth_app.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.http import Http404
from django.db import transaction
from django.db.models import Sum
from productadmin.models import ProductVariant
# Create your views here.


class UserProfileUpdateView(APIView):
    def put(self, request, format=None):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        user = user_profile.user
        user_profile.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CartView(APIView):
    def get_object(self, user_id, item_id=None):
        if item_id:
            try:
                return CartItem.objects.get(user_id=user_id, pk=item_id, is_ordered=False)
            except CartItem.DoesNotExist:
                raise Http404("Cart item not found.")
        return CartItem.objects.filter(user_id=user_id, is_ordered=False)

    def get(self, request, user_id, item_id=None, format=None):
        cart_items = self.get_object(user_id, item_id)
        many = not item_id
        serializer = CartItemSerializer(cart_items, many=many)
        
        if many:
            subtotal = self.calculate_subtotal(cart_items)
            response_data = {
                'cart_items': serializer.data,
                'subtotal': subtotal
            }
            return Response(response_data)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        user = User.objects.get(pk=user_id)
        data = request.data.copy()
        item_id = data.get('item')
        
        try:
            # Check if the cart item already exists
            existing_cart_item = CartItem.objects.get(user=user, item_id=item_id, is_ordered=False)
            existing_cart_item.quantity += data.get('quantity', 1)  # Default to 1 if quantity is not provided
            existing_cart_item.save()
            serializer = CartItemSerializer(existing_cart_item)
        except CartItem.DoesNotExist:
            # If it doesn't exist, create a new cart item
            data['user'] = user.id 
            serializer = CartItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id, item_id, format=None):
        cart_item = self.get_object(user_id, item_id)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, item_id, format=None):
        cart_item = self.get_object(user_id, item_id)
        cart_item.delete()
        
        remaining_cart_items = self.get_object(user_id)
        serializer = CartItemSerializer(remaining_cart_items, many=True)
        subtotal = self.calculate_subtotal(remaining_cart_items)
        response_data = {
            'cart_items': serializer.data,
            'subtotal': subtotal
        }
        
        return Response(response_data)

    def calculate_subtotal(self, cart_items):
        return sum(item.total_price for item in cart_items)

class WishlistView(APIView):   
    def get(self, request, user_id, format=None):
        wishlist_items = WishList.objects.filter(user_id=user_id)
        serializer = WishlistItemSerializer(wishlist_items, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        user = User.objects.get(pk=user_id)
        data = request.data.copy()
        product_id = data.get('product')

        try:
            existing_wishlist_item = WishList.objects.get(user=user, product_id=product_id)
            return Response({"detail": "Product already exists in wishlist."}, status=status.HTTP_400_BAD_REQUEST)
        except WishList.DoesNotExist:
            product = ProductVariant.objects.get(pk=product_id)
            wishlist_data = {'user': user.id, 'product': product.id}
            serializer = WishlistItemSerializer(data=wishlist_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, item_id, format=None):
        try:
            wishlist_item = WishList.objects.get(user_id=user_id, pk=item_id)
            wishlist_item.delete()
            remaining_wishlist_items = WishList.objects.filter(user_id=user_id)
            serializer = WishlistItemSerializer(remaining_wishlist_items, many=True)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except WishList.DoesNotExist:
            return Response({"detail": "Wishlist item not found."}, status=status.HTTP_404_NOT_FOUND)
        
class CheckOutView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = CartItem.objects.filter(user=user, is_ordered=False)
        
        if not cart_items.exists():
            return Response({"error": "No items to checkout."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Process each cart item
                for cart_item in cart_items:
                    # Update stock and mark as ordered
                    cart_item.item.stock -= cart_item.quantity
                    cart_item.item.save()
                    cart_item.is_ordered = True
                    cart_item.save()
                    
                    # Create Checkout record
                    CheckOut.objects.create(
                        order=cart_item,
                        first_name=request.data.get('first_name'),
                        last_name=request.data.get('last_name'),
                        email=request.data.get('email'),
                        address=request.data.get('address'),
                        mobile_no=request.data.get('mobile_no'),
                        company_name=request.data.get('company_name'),
                        country=request.data.get('country'),
                        city=request.data.get('city'),
                        state=request.data.get('state'),
                        postal_code=request.data.get('postal_code')
                    )
                
                # Return success response
                return Response({"message": "Checkout successful."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Fetch user object based on user_id
            user = get_object_or_404(User, id=user_id)
            
            # Retrieve CheckOut instances for the specified user
            checkouts = CheckOut.objects.filter(order__user=user)
            serializer = CheckOutSerializer(checkouts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LatestProductView(APIView) :
    def get(self, request) :
        latest_product = ProductVariant.objects.order_by('-id')[:3]
        serializer = ProductDisplaySerializer(latest_product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BestSellerView(APIView) :
    def get(self, request) :
        bestsellers = ProductVariant.objects.filter(cartitem__is_ordered=True)\
                                            .annotate(total_ordered=Sum('cartitem__quantity'))\
                                            .order_by('-total_ordered')[:3]
        serializer = ProductDisplaySerializer(bestsellers, many=True)   
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FeaturedProductView(APIView) :
    def get(self, request) :
        featured_product = ProductVariant.objects.filter(is_featured=True).order_by('-id')[:3]
        serializer = ProductDisplaySerializer(featured_product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TrendingProductView(APIView) :
    def get(self, request) :
        trending_product = ProductVariant.objects.filter(cartitem__is_ordered=True)\
                                            .annotate(total_ordered=Sum('cartitem__quantity'))\
                                            .order_by('-total_ordered')[:10]
        serializer = ProductDisplaySerializer(trending_product, many=True)   
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView) :
    def get(self, request, product_id) :
        try :
            product = ProductVariant.objects.get(id=product_id)
            serializer = ProductDisplaySerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except :
            return Response({"error" : "Product not found"}, status=status.HTTP_404_NOT_FOUND)