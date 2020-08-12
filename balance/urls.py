from django.urls import path
from . import viewsets

urlpatterns = [
    path('promo_code/', viewsets.redeem),
]
