from datetime import date

from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Main serializer for the creation and validation of a complete user,
    including sensitive fields such as password and date of birth.
    """
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'password',
                  'email',
                  'birth_date',
                  'can_be_contacted',
                  'can_data_be_shared'
                  ]

    @staticmethod
    def validate_birth_date(value):
        """
        Valid that the user is at least 15 years old on the current date.
        Raises a ValidationError if not.
        """
        today = date.today()
        age = today.year - value.year - (
                    (today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour créer un compte.")
        return value

    def create(self, validated_data):
        """
        Creates a new user with a hashed password from the validated data.
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer used to display a public or restricted view of the user.
    Does not contain sensitive data (e.g. password or email).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'can_be_contacted', 'can_data_be_shared']
