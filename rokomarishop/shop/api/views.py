from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializer import RegistrationSerializer, AccountUpdateSerializer, AccountFullSerializer
from ..models import Account, Profile
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
import uuid


@api_view(['POST',])
@permission_classes([AllowAny,])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0')
        if validate_email(email) != None:
            data['error_message'] = 'Email Already In Use.'
            data['response'] = 'Error.'
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        username = request.data.get('username', '0')
        if validate_username(username) != None:
            data['error_message'] = "Username Already In Use."
            data['response'] = "Error"
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            #sending response back to the user
            data['response'] = 'successfully registered new user.'
            data['pk'] = account.pk
            data['username'] = account.username
            data['mobile'] = account.mobile
            data['seller'] = account.seller
            data['customer'] = account.customer
            token = Token.objects.get(user=account).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email

def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username



@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def account_update_view(request):
    data = {}
    pk = request.query_params.get('pk', '0')
    try:
        val = uuid.UUID(pk, version=4)
    except ValueError:
        data['error_message'] = "invalid uuid"
        data['message'] = "pk error."
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        data['error_message'] = "can't find account with that pk."
        data['message'] = "no user"
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    serializer = AccountUpdateSerializer(account, data=request.data)
    if account != request.user:
        return Response({"message": "don't have permission."}, status=status.HTTP_401_UNAUTHORIZED)
    if serializer.is_valid():
        user = serializer.save()
        data['username'] = user.username
        data['mobile'] = user.mobile
        data['customer'] = user.customer
        data['seller'] = user.seller
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def user_full_details(request):
    data = {}
    pk = request.query_params.get('pk', '0')
    try:
        val = uuid.UUID(pk, version=4)
    except ValueError:
        data['error_message'] = "invalid uuid"
        data['message'] = "pk error."
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        data['error_message'] = "can't find account with that pk."
        data['message'] = "no user"
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if account != request.user:
        return Response({"message": "don't have permission."}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = AccountFullSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)


