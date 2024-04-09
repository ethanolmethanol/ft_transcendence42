from django.urls import path
from .views import health, join

urlpatterns = [
    path('health/', health, name='health-check'),
    path('join/', join, name='join'),
]
