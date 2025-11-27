from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [

    # Tested
    path("login/", TokenObtainPairView.as_view(), name="login"),
    # Tested
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Tested
    path("logout/", LogoutView.as_view(), name="logout"),
    # Admin only - Tested
    path("register/", UserRegisterView.as_view(), name="register"),
    # Logged-in user - Tested
    path("profile/", ShowProfileDetail.as_view(), name="profile"),
    # Admin only - Tested
    path("allusers/", ShowAllUsersView.as_view(), name="all_users"),
]
