from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Fetch the user by email
        try:
            user = User.objects.get(email=email)
            print("Found user:", user, password, user.password)  # Debugging line
        except User.DoesNotExist:
            raise serializers.ValidationError("Email does not exist")

        # Check if the password matches the hashed password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid password")

        # Add user to validated attrs for use in the view
        attrs['user'] = user
        return attrs
