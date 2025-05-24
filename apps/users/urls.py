# apps/users/urls.py
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path("login/", views.user_login, name="login"),
    path("password-reset/", views.password_reset, name="password-reset"),
    
    # Add other endpoints:
    # path("register/", views.user_register, name="register"),
]