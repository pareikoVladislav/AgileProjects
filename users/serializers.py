import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
# from rest_framework.exceptions import ValidationError

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    current_project = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'position',
            'email',
            'phone',
            'last_login',
            'current_project',
        ]

class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'position',
            'password',
            're_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        username = attrs['username']
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        password = attrs['password']
        re_password = attrs.pop('re_password')

        if not re.match('^[a-zA-Z_0-9]*$', username):
            raise serializers.ValidationError("Никнэйм должен содержать: любые буквы из латиницы, символ нижнего подчёркивания, цифры от 0 до 9")

        if not first_name.isalpha():
            raise serializers.ValidationError("Имя должно содержать cтрого буквы из латиницы, любым регистром")

        if not last_name.isalpha():
            raise serializers.ValidationError("Фамилия должна содержать cтрого буквы из латиницы, любым регистром")

        if password != re_password:
            raise serializers.ValidationError("Пароль и его повторный ввод должны совпадать")

        try:
            validate_password(password)
        except serializers.ValidationError as err:
            raise serializers.ValidationError(err.messages)

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



