from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductAdminAddSerializers
from rest_framework import status
# Create your views here.


class CreateProductAdminView(APIView):
    def post(self,requset,*args,**kwargs):
        serializer=ProductAdminAddSerializers(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
