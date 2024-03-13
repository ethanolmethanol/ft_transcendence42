from django.urls import path
from .views import signin, signup, logout

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
]