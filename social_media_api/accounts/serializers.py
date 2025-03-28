from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Extract password to hash it later
        password = validated_data.pop('password')

        # Create a new user using the custom manager's create_user method
        user = User.objects.create_user(**validated_data)
        
        # Set the password hash (if not using create_user(), the password wouldn't be hashed)
        user.set_password(password)
        user.save()

        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return user, token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Retrieve the user by the username
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):  # Verify the password
            # If password matches, generate a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token.key}

        # Raise an error if username or password is invalid
        raise serializers.ValidationError('Invalid username or password')