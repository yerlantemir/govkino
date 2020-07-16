from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import User
from .serializers import UsersSerializer
from .utils import generate_pin

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UsersListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class SMSSignInView(APIView):

    def post(self, request):
        user_data = request.data

        if 'username' in user_data:
            user = User.objects.filter(username=user_data['username'])
        elif 'phone_number' in user_data:
            user = User.objects.filter(phone_number=user_data['phone_number'])
        else:
            raise ValidationError("No username or phone_number in query body")

        if user.exists():
            verification_code = generate_pin()
            # sending to user
            print(verification_code)
            cache.set(verification_code, user[0])
        else:
            raise ValidationError("No such user in DB")
        return Response({"status": "validation code sent", "code": verification_code}, status=status.HTTP_200_OK)


class SMSSignInVerificationView(APIView):

    def post(self, request):
        user_data = request.data

        if 'code' in user_data:

            verification_code = user_data['code']
            user = cache.get(verification_code)

            if user:
                token = Token.objects.create(user=user)
                token.save()
            else:
                raise ValidationError("Verification code does not exist")
        else:
            raise ValidationError("No verification code in query body")

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class PasswordSignInView(APIView):

    def post(self, request):
        user_data = request.data
        print(user_data.get('username'), 'heeeeeeeeeey')
        try:
            if 'username' in user_data:
                user = User.objects.get(username=user_data.get('username'), password=user_data.get('password'))
            elif 'phone_number' in user_data:
                user = User.objects.get(phone_number=user_data.get('phone_number'), password=user_data.get('password'))
        except User.DoesNotExist:
            raise ValidationError("No username or password in query body")

        if user:
            token = Token.objects.create(user=user)
            token.save()
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            raise ValidationError("No such user in DB")


class SignUpView(APIView):

    def post(self, request):

        user_data = request.data
        serializer = UsersSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        username = user_data.get('username')
        phone_number = user_data.get('phone_number')
        password = user_data.get('password')

        duplicate_user = User.objects.filter(username=username, phone_number=phone_number)
        if duplicate_user.exists():
            raise ValidationError("user with the same username and phone number already exists")

        user = User(username=username, password=password, phone_number=phone_number)

        code = generate_pin()
        cache.set(code, user)
        print("Pin code:", code)

        return Response({'message': 'check verification code', 'code': code}, status=status.HTTP_201_CREATED)


class SignUpVerificationView(APIView):

    def post(self, request):
        pin_code = request.data.get('code')
        user = cache.get(pin_code)
        if user:
            user.save()
        else:
            raise ValidationError("Incorrect pin_code")
        return Response({"message": "user created"}, status=status.HTTP_201_CREATED)


class SignOutView(APIView):

    def post(self, request):
        user_data = request.data

        if 'token' in user_data:
            Token.delete(user_data.get('token'))
            return Response({"message": "signed out"}, status.HTTP_200_OK)
        else:
            raise ValidationError('No token provided')