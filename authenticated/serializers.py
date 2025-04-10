from datetime import date

from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'birth_date', 'can_be_contacted', 'can_data_be_shared']

    def validate_birth_date(self, value):
        """Verify that the user is at least 15 years old."""
        today = date.today()
        age = today.year - value.year - (
                    (today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour créer un compte.")
        return value

    def create(self, validated_data):
        """Crée un utilisateur avec un mot de passe haché."""
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'can_be_contacted', 'can_data_be_shared']
