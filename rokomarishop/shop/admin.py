from django.contrib import admin
from .models import Account
from .models import Profile
# Register your models here.

admin.site.register(Account)
admin.site.register(Profile)