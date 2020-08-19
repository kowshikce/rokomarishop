from django.urls import path
from .views import registration_view
from .views import account_update_view
from .views import user_full_details
from django.conf import settings


urlpatterns = [
    path('api/v1/registration/', registration_view, name="registration"),
    path('api/v1/update/', account_update_view, name="update profile"),
    path('api/v1/details/', user_full_details, name="detailed user view"),
]
