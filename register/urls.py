from django.urls import path
from .views import user_register,user_login,user_logout,register_profile

urlpatterns = [
    path('', user_login, name = 'user_login'),
    path('register/', user_register, name = 'user_register'),
    path('logout/', user_logout, name = 'logout'),
    path('register_profile/', register_profile, name='register_profile'),
]