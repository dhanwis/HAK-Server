from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
# Create your views here.

###############################################CategoryManagement#########################################################


# GET /categories/ for listing all categories
# POST /categories/ for creating a new category
# GET /categories/{id}/ for retrieving a single category by ID
# PUT /categories/{id}/ for updating a category by ID
# PATCH /categories/{id}/ for partially updating a category by ID
# DELETE /categories/{id}/ for deleting a category by ID

# {
#   "name": "Books"
#   "image":"path"
# }

class CategoryViewSet(ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    
######################################################SubCategoryManagement#######################################

# GET /products/ - List all products
# POST /products/ - Create a new product
# GET /products/{id}/ - Retrieve a single product by ID
# PUT /products/{id}/ - Update a product by ID
# PATCH /products/{id}/ - Partially update a product by ID
# DELETE /products/{id}/ - Delete a product by ID

# {
#   "category": 1,
#   "name": "Smartphone",
#   "description": "A smartphone with many features."
# }


class ProductViewSet(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()




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
# Update a color image by ID: PUT /color-images/{id}/
# Partial update of a color image by ID: PATCH /color-images/{id}/
# Delete a color image by ID: DELETE /color-images/{id}/

# {
#   "image": "http://example.com/media/color/color1.jpg",
#   "name": "Color 1"
# }


class ColorImageViewset(ModelViewSet):
    serializer_class=ColorImageSerializer
    queryset=ColorImage.objects.all()
    

#################################################