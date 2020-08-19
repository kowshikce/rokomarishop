from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
import uuid


# Create your models here.


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, mobile, customer, seller, password=None):
        if not email:
            raise ValueError("Email Must Be Provided.")
        if not username:
            raise ValueError("Username Must Be Provided.")

        user = self.model(email=self.normalize_email(email), username=username, mobile=mobile, customer=customer,
                          seller=seller)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile, customer, seller, password):
        user = self.create_user(email=self.normalize_email(email), username=username, mobile=mobile, customer=customer,
                                seller=seller, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(blank=False, default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=128, unique=True)
    customer = models.BooleanField(default=False)
    seller = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'mobile', 'customer', 'seller']

    objects = MyAccountManager()

    def __str__(self):
        return "{x}({y})".format(x=self.username, y=self.id)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    user_device = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
