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
        # Create user with the provided data
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        # Create a token for the newly created user
        token, created = Token.objects.get_or_create(user=user)
        
        return user, token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Check if username and password are correct
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            # If correct, create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token.key}

        raise serializers.ValidationError('Invalid username or password')