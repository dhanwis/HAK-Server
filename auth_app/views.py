from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from .models import User, UserProfile
from .serializers import UserProfileSerializer
from .utils import send_otp
import random
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication




class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response("Phone number is required", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            user = User.objects.create(phone_number=phone_number)

        # Generate OTP and update user record
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.save()

        # Function to send OTP, adjust this according to your sending method
        send_otp(user.phone_number, otp)

        return Response({"message": "Successfully generated OTP", "customer_id": user.id}, status=status.HTTP_200_OK)
    
    
    
class CustomerVerifyOTP(APIView):
    def patch(self, request, customer_id=None, format=None):
        try:
            user = get_object_or_404(User, id=customer_id)
            otp = request.data.get("otp")

            if user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # User is already active, update OTP-related fields and generate token
                user.otp = ""
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp': 'Successfully verified the customer',
                    'message': 'The customer already exists'
                }
                return Response(data, status=status.HTTP_200_OK)

            elif not user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # OTP verification successful, activate user and generate token
                user.is_active = True
                user.otp = ""
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp': 'Successfully verified the customer',
                    'message': 'New customer'
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response("Incorrect OTP.", status=status.HTTP_400_BAD_REQUEST)
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
            return Response("Successfully generated new OTP.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save(user=request.user)

            # Retrieve the user's access token
            access_token = AccessToken().for_user(request.user)

            response_data = {
                'profile': serializer.data,
                'access_token': str(access_token),
            }

            print(response_data)
            return Response(response_data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

               
    
    
