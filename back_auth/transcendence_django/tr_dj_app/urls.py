from django.urls import path
from .views import signin
from .views import signup

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
]