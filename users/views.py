from typing import Any, TYPE_CHECKING, cast

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    SetPinSerializer,
    VerifyPinSerializer,
)

if TYPE_CHECKING:
    # For type checkers: reference the actual custom user model
    from .models import User as CustomUser

User = get_user_model()


# ---------------------------
# User Registration
# ---------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ---------------------------
# Step 1: Login
# ---------------------------
class LoginView(APIView):
    """
    Step 1: User submits email/username & password.
    If 2FA is enabled, return `two_factor_required: True`.
    Else, return JWT tokens directly.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Pylance: we know this is our custom user at runtime
        cu = cast("CustomUser", user)

        # Check if 2FA is enabled (fix: correct field name)
        if getattr(cu, "two_factor_enabled", False):
            token = get_random_string(6, allowed_chars="0123456789")
            # Cast to Any to quiet Pylance about dynamic attributes on AbstractUser
            cast(Any, cu).two_factor_token = token
            cu.save()
            send_mail(
                "Your 2FA Code",
                f"Your verification code is {token}",
                settings.DEFAULT_FROM_EMAIL,
                [cu.email],
            )
            return Response({"two_factor_required": True}, status=status.HTTP_200_OK)

        # No 2FA: return tokens immediately
        refresh = RefreshToken.for_user(cu)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


# ---------------------------
# Step 2: 2FA Verification
# ---------------------------
class TwoFAVerifyView(APIView):
    """
    Step 2: User submits username & 2FA code.
    """

    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        try:
            user = User.objects.get(username=username, two_factor_token=code)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        cu = cast("CustomUser", user)

        # Clear the 2FA token
        cast(Any, cu).two_factor_token = ""
        cu.save()

        refresh = RefreshToken.for_user(cu)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


# ---------------------------
# Profile
# ---------------------------
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):  # type: ignore[override]
        return self.request.user


# ---------------------------
# Step 1: Request PIN Token
# ---------------------------
class RequestPinTokenView(APIView):
    """
    Sends a one-time token to user's email to verify before setting/changing PIN.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cu = cast("CustomUser", request.user)
        token = get_random_string(6, allowed_chars="0123456789")
        cast(Any, cu).pin_reset_token = token
        cu.save()

        send_mail(
            "PIN Setup Verification",
            f"Your PIN setup token is: {token}",
            settings.DEFAULT_FROM_EMAIL,
            [cu.email],
        )
        return Response({"detail": "PIN token sent to your email"})


# ---------------------------
# Step 2: Set PIN
# ---------------------------
class SetPinView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SetPinSerializer

    def update(self, request, *args, **kwargs):
        cu = cast("CustomUser", request.user)
        token = request.data.get("token")
        if token != getattr(cu, "pin_reset_token", ""):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        response = super().update(request, *args, **kwargs)

        # Clear token after successful PIN set
        cast(Any, cu).pin_reset_token = ""
        cu.save()
        return response


# ---------------------------
# Verify PIN (For Withdrawals)
# ---------------------------
class VerifyPinView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyPinSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "PIN verified"})
