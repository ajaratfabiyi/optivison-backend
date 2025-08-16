from typing import Any, TYPE_CHECKING, cast
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

if TYPE_CHECKING:
    # This lets Pylance know about your real user model
    from .models import User as CustomUser

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "referred_by"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        cu = cast("CustomUser", user)

        # If 2FA is enabled, return flag instead of tokens immediately
        if getattr(cu, "two_factor_enabled", False):
            # Local fallback for OTP generation if utils is missing
            from django.utils.crypto import get_random_string

            try:
                from .utils import generate_otp
            except ImportError:
                def generate_otp(length: int = 6) -> str:
                    return get_random_string(length, allowed_chars="0123456789")

            token = generate_otp()
            cast(Any, cu).two_factor_token = token
            cu.save()
            # TODO: Send token via email or SMS here
            return {"two_factor_required": True, "user_id": str(cu.id)}

        refresh = RefreshToken.for_user(cu)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class TwoFAVerifySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs["user_id"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID.")

        cu = cast("CustomUser", user)

        if getattr(cu, "two_factor_token", None) != attrs["token"]:
            raise serializers.ValidationError("Invalid or expired 2FA token.")

        # Clear the token after use
        cast(Any, cu).two_factor_token = None
        cu.save()

        refresh = RefreshToken.for_user(cu)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "referral_code", "is_kyc_verified"]


class RequestPinTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        cu = cast("CustomUser", user)

        try:
            from .utils import generate_otp
        except ImportError:
            from django.utils.crypto import get_random_string

            def generate_otp(length: int = 6) -> str:
                return get_random_string(length, allowed_chars="0123456789")

        token = generate_otp()
        cast(Any, cu).pin_reset_token = token
        cu.save()
        # TODO: send token to email/SMS
        return {"detail": "PIN token sent."}


class SetPinSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    pin = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        cu = cast("CustomUser", user)

        if getattr(cu, "pin_reset_token", None) != attrs["token"]:
            raise serializers.ValidationError("Invalid PIN token.")

        cu.set_pin(attrs["pin"])
        cast(Any, cu).pin_reset_token = None
        cu.save()
        return {"detail": "PIN set successfully."}


class VerifyPinSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pin = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        cu = cast("CustomUser", user)

        if not cu.check_pin(attrs["pin"]):
            raise serializers.ValidationError("Invalid PIN.")
        return {"detail": "PIN verified successfully."}
