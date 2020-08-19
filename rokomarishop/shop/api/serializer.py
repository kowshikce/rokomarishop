from rest_framework import serializers
from ..models import Account, Profile
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'mobile', 'customer', 'seller')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account(email=validated_data['email'],
                       username=validated_data['username'],
                       mobile=validated_data['mobile'],
                       customer=validated_data['customer'],
                       seller=validated_data['seller'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccountUpdateSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=128, required=False)
    username = serializers.CharField(max_length=50, required=False)
    seller = serializers.BooleanField(required=False)
    customer = serializers.BooleanField(required=False)

    class Meta:
        model = Account
        fields = ('customer', 'seller', 'mobile', 'username')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birthday')


class AccountFullSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'mobile', 'customer', 'seller', 'profile', 'date_created', 'last_login',
                  'is_active', 'is_admin', 'is_staff', 'is_superuser')
