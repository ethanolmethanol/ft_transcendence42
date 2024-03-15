from django.urls import path
from .views import signin, signup, check_username_availability, check_email_availability

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('check-username/<str:username>/', check_username_availability, name='check_username_availability'),
    path('check-email/<str:email>/', check_email_availability, name='check_email_availability'),
]