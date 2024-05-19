# Importing modules from DRF
from rest_framework import serializers
from authentication.models import CustomUser
from wallet.serializers import WalletSerializer


# Serializer for user registration
class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# List user serializer
class UserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = CustomUser
        fields = ["id", "email", "wallet"]
