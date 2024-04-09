from django.urls import path
from .views import join

urlpatterns = [
    path('join/', join, name='join'),
]
