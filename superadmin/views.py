from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductAdminAddSerializers,ProductAdminProfileSerializer,OrderAdminProfileSerializer,OrderAdminAddSerializers, SalesAdminAddSerializer, SalesAdminProfileSerializer, OrderStatusChangeSerializer
from rest_framework import status
from auth_app.models import User ,UserProfile
from django.shortcuts import get_object_or_404
from django.http import Http404
from productadmin.models import *
from auth_app.serializers import UserProfileSerializer
from client.models import CheckOut
from client.serializers import CheckOutSerializer
# Create your views here.

###############################################ProductAdminManagemet#####################################################
class CreateProductAdminView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=ProductAdminAddSerializers(data=request.data)
        if serializer.is_valid():       
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class ProductAdminProfile(APIView):
    
    def get(self,request,pk):
        admin=get_object_or_404(User,pk=pk,is_product_admin=True)
        serializer=ProductAdminProfileSerializer(admin)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk,*args,**kwargs):
        admin=get_object_or_404(User,pk=pk,is_product_admin=True)
        serializer=ProductAdminProfileSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        admin = get_object_or_404(User, pk=pk,is_product_admin=True)
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
        admin=get_object_or_404(User,pk=pk,is_order_admin=True)
        serializer=OrderAdminProfileSerializer(admin)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request,pk,*args,**kwargs):
        admin=get_object_or_404(User,pk=pk,is_order_admin=True)
        serializer=OrderAdminProfileSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        admin = get_object_or_404(User, pk=pk,is_order_admin=True)
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
    
############################################## salesadminmanagemant #################################################

class CreateSalesAdminView(APIView) :
    def post(self, request, *args, **kwargs) :
        serializer = SalesAdminAddSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SalesAdminProfileView(APIView) :
    def get(self, request, pk) :    
        admin = get_object_or_404(User, pk=pk, is_sales_admin=True)
        serializer = SalesAdminProfileSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request,pk,*args,**kwargs):
        admin=get_object_or_404(User,pk=pk,is_sales_admin=True)
        serializer=SalesAdminProfileSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk, *args, **kwargs) :
        admin = get_object_or_404(User, pk=pk, is_sales_admin=True)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##################################### Order Status Change ##########################################

class OrderStatusChangeAPIView(APIView):
    def get_object(self, pk):
        try:
            return CheckOut.objects.get(pk=pk)
        except CheckOut.DoesNotExist:
            raise Http404("No order found")
        
    def patch(self, request, pk, format=None):
        checkout = self.get_object(pk)
        serializer = OrderStatusChangeSerializer(checkout, data=request.data, partial=True)
        if serializer.is_valid():
            if request.user.is_authenticated and (request.user.is_superuser or request.user.is_order_admin):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'detail': "You don't have the permission"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AllOrderView(APIView) :
    def get(self, request, format=None) :
        checkout = CheckOut.objects.all()
        serializer = CheckOutSerializer(checkout, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

