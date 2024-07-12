from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductAdminAddSerializers,ProductAdminProfileSerializer,OrderAdminProfileSerializer,OrderAdminAddSerializers
from rest_framework import status
from auth_app.models import User ,UserProfile
from django.shortcuts import get_object_or_404
from django.http import Http404
from productadmin.models import *
from auth_app.serializers import UserProfileSerializer
# Create your views here.

###############################################ProductAdminManagemet#####################################################
class CreateProductAdminView(APIView):
    def post(self,requset,*args,**kwargs):
        serializer=ProductAdminAddSerializers(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class ProductAdminProfile(APIView):
    
    def get(self,request,pk):
        admin=get_object_or_404(UserProfile,pk=pk,is_product_admin=True)
        serializer=ProductAdminProfileSerializer(admin)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk,*args,**kwargs):
        admin=get_object_or_404(UserProfile,pk=pk,is_product_admin=True)
        serializer=ProductAdminProfileSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        admin = get_object_or_404(UserProfile, pk=pk,is_product_admin=True)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
########################################OrderAdminManagement######################################################


class CreateOrderAdminView(APIView):
    def post(self,requset,*args,**kwargs):
        serializer=OrderAdminAddSerializers(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class OrderAdminProfile(APIView):
    
    def get(self,request,pk):
        admin=get_object_or_404(UserProfile,pk=pk,is_order_admin=True)
        serializer=OrderAdminProfileSerializer(admin)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk,*args,**kwargs):
        admin=get_object_or_404(UserProfile,pk=pk,is_order_admin=True)
        serializer=OrderAdminProfileSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        admin = get_object_or_404(UserProfile, pk=pk,is_order_admin=True)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
##################################################USER MANAGEMENT#################################################

class DeactivateCustomerAPIView(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_customer=True)
        except User.DoesNotExist:
            raise Http404("Customer not found.")
        user.is_active = False
        user.save()
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response({'message': 'Customer deactivated.', 'profile': serializer.data}, status=status.HTTP_200_OK)

    
    def delete(self,request,pk):
        try:
            user=User.object.get(pk=pk,is_customer=True)
        except User.DoesNotExist:
            raise Http404("Customer not found")
        user.delete()
        return Response(status=status.HTTP_200_OK)
    


