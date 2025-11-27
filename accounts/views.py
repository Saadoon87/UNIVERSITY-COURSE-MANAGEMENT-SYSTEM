from rest_framework import generics, permissions, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


# ADMIN-ONLY PERMISSION
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "ADMIN"
        )


# REGISTER (ADMIN ONLY)
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdmin]


# SHOW ALL USERS (ADMIN ONLY)
class ShowAllUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]


# SHOW LOGGED-IN USER DETAILS
class ShowProfileDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


# LOGOUT
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response({"message": "Logout successful & Token been blacklisted"}, status=status.HTTP_205_RESET_CONTENT)

        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        except (TokenError, InvalidToken):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
