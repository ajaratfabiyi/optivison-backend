from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Referral

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(required=True)  # ✅ Now required

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'referral_code']

    def validate_referral_code(self, value):
        """
        Ensure the referral code exists before proceeding.
        """
        try:
            self.referrer = User.objects.get(referral_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code.")
        return value

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code')
        password = validated_data.pop('password')

        # Create the user
        user = User(**validated_data)
        user.set_password(password)
        user.referred_by = self.referrer
        user.save()

        # Create referral link record
        Referral.objects.create(referrer=self.referrer, referred=user)

        return user


class SetPinSerializer(serializers.Serializer):
    pin = serializers.CharField(min_length=4, max_length=6)


class VerifyPinSerializer(serializers.Serializer):
    pin = serializers.CharField(min_length=4, max_length=6)
