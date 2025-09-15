from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/signup/', user_signup, name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
]