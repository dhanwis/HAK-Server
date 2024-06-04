from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from .models import User, UserProfile
from .serializers import CustomerSerializer, UserProfileSerializer
from .utils import send_otp
import random
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login


class CustomerListCreate(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.filter(is_customer=True)
            if not users.exists():
                return Response({"message": "The customer is empty"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve customers: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create customer: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerVerifyOTP(APIView):
    def patch(self, request, customer_id=None, format=None):
        try:
            user = get_object_or_404(User, id=customer_id)
            otp = request.data.get("otp")

            if user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # User is already active, update OTP-related fields and generate token
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp' : 'Successfully verified the customer',
                    'message' : 'The customer already exists'
                }
                return Response(data, status=status.HTTP_200_OK)

            elif not user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # OTP verification successful, activate user and generate token
                user.is_active = True
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp' : 'Successfully verified the customer',
                    'message' : 'New customer'
                }
                return Response(data,  status=status.HTTP_201_CREATED)
            else:
                return Response("incorrect OTP.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Something went wrong: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerRegenerateOTP(APIView):
    def patch(self, request, customer_id=None, format=None):
        try:
            user = get_object_or_404(User, id=customer_id)

            if int(user.max_otp_try) == 0 and timezone.now() < user.otp_max_out:
                return Response(
                    "Max OTP try reached, try after an hour",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            max_otp_try = int(user.max_otp_try) - 1

            user.otp = otp
            user.otp_expiry = otp_expiry
            user.max_otp_try = max_otp_try

            if max_otp_try == 0:
                otp_max_out = timezone.now() + datetime.timedelta(hours=1)
                user.otp_max_out = otp_max_out
            elif max_otp_try == -1:
                user.max_otp_try = settings.MAX_OTP_TRY
            else:
                user.otp_max_out = None
                user.max_otp_try = max_otp_try

            user.save()
            send_otp(user.phone_number, otp)
            return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class UserProfileGetAdd(APIView):
    def post(self, request, format=None):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        street = request.data.get('street')
        city = request.data.get('city')
        state = request.data.get('state')
        pincode = request.data.get('pincode')
        user = request.user
        try:
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                street=street,
                city=city,
                state=state,
                pincode=pincode
            )
            user_profile_serializer = UserProfileSerializer(user_profile)
            return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
