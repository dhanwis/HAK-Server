from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from auth_app.models import UserProfile,User
from auth_app.serializers import UserProfileSerializer
# Create your views here.

###############################################CategoryManagement#########################################################


# GET /categories/ for listing all categories
# POST /categories/ for creating a new category
# GET /categories/{id}/ for retrieving a single category by ID
# PATCH /categories/{id}/ for partially updating a category by ID
# DELETE /categories/{id}/ for deleting a category by ID

# {
#   "name": "Books"
#   "image":"path"
# }

class CategoryList(APIView):
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
######################################################SubCategoryManagement#######################################

# GET /products/ - List all products
# POST /products/ - Create a new product
# GET /products/{id}/ - Retrieve a single product by ID
# PATCH /products/{id}/ - Partially update a product by ID
# DELETE /products/{id}/ - Delete a product by ID

# {
#   "category": 1,
#   "name": "Smartphone",
#   "description": "A smartphone with many features."
# }


class ProductAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404




###################################################SizeManagement##########################################################

# List all sizes: GET /sizes/
# Create a new size: POST /sizes/
# Retrieve a size by ID: GET /sizes/{id}/
# Update a size by ID: PUT /sizes/{id}/
# Partial update of a size by ID: PATCH /sizes/{id}/
# Delete a size by ID: DELETE /sizes/{id}/


# {
#   "name": "Small"
# }


class SizeViewSet(ModelViewSet):
    serializer_class=SizeSerializer
    queryset=Size.objects.all()
    



####################################################ColorImageManagement####################################################

# List all color images: GET /color-images/
# Create a new color image: POST /color-images/
# Retrieve a color image by ID: GET /color-images/{id}/
# Partial update of a color image by ID: PATCH /color-images/{id}/
# Delete a color image by ID: DELETE /color-images/{id}/

# {
#   "image": "http://example.com/media/color/color1.jpg",
#   "name": "Color 1"
# }


class ColorImageAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            color_image = self.get_object(pk)
            serializer = ColorImageSerializer(color_image)
            return Response(serializer.data)
        else:
            color_images = ColorImage.objects.all()
            serializer = ColorImageSerializer(color_images, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ColorImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        color_image = self.get_object(pk)
        serializer = ColorImageSerializer(color_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        color_image = self.get_object(pk)
        color_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return ColorImage.objects.get(pk=pk)
        except ColorImage.DoesNotExist:
            raise Http404
    

#################################################ColourManagement########################################
# GET /colors/: Retrieves a list of all colors.
# POST /colors/: Creates a new color.
# GET /colors/{id}/: Retrieves details of a specific color.
# PATCH /colors/{id}/: Partially updates a specific color.
# DELETE /colors/{id}/: Deletes a specific color.


# {
#   "product": 2,
#   "name": "Blue",
#   "images": [
#     {"image": "img/color/blue1.jpg"},
#     {"image": "img/color/blue2.jpg"}
#   ]
# }


class ColorAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            color = self.get_object(pk)
            serializer = ColorSerializer(color)
            return Response(serializer.data)
        else:
            colors = Color.objects.all()
            serializer = ColorSerializer(colors, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        color = self.get_object(pk)
        serializer = ColorSerializer(color, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        color = self.get_object(pk)
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return Color.objects.get(pk=pk)
        except Color.DoesNotExist:
            raise Http404


#############################################ProductVarientManagement############################################

# GET /product-variants/: Retrieves a list of all product variants.
# POST /product-variants/: Creates a new product variant.
# GET /product-variants/{id}/: Retrieves details of a specific product variant.
# PATCH /product-variants/{id}/: Partially updates a specific product variant.
# DELETE /product-variants/{id}/: Deletes a specific product variant.

# {
#   "product": 1,
#   "size": 2,
#   "color": 3,
#   "actual_price": "49.99",
#   "discount_price": "39.99",
#   "stock": 100
# }


class ProductVariantAPIView(APIView):
    
    def get(self, request, pk=None):
        if pk:
            product_variant = self.get_object(pk)
            serializer = ProductvarientSerializer(product_variant)
            return Response(serializer.data)
        else:
            product_variants = ProductVariant.objects.all()
            serializer = ProductvarientSerializer(product_variants, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductvarientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product_variant = self.get_object(pk)
        serializer = ProductvarientSerializer(product_variant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product_variant = self.get_object(pk)
        product_variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return ProductVariant.objects.get(pk=pk)
        except ProductVariant.DoesNotExist:
            raise Http404



class CustomerProfilesAPIView(APIView):

    def get(self, request):
        customers = User.objects.filter(is_customer=True)
        profiles = UserProfile.objects.filter(user__in=customers)
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)