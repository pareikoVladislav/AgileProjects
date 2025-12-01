import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User

class UserListSerializer(serializers.ModelSerializer):
    current_project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "position",
            "email",
            "phone",
            "last_login",
            "current_project"
        ]
# Создайте новый сериализатор RegisterUserSerializer для регистрации нового пользователя. Сериализатор будет обрабатывать поля:
# username
# first_name
# last_name
# email
# position
# password
# re_password
# Поле re_password - искусственно созданное поле для проверки совпадения паролей, содержит настройки:
# Максимальная длина - 128 символов
# Только для записи
# В параметре extra_kwargs указать, что поле password строго только для записи.
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
            're_password'
             ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        username = attrs['username']
        first_name   = attrs['first_name']
        last_name   = attrs['last_name']
        # email   = attrs['email']
        # position    = attrs['position']
        password    = attrs['password']
        re_password    = attrs.pop['re_password']

        if re.match('^[a-z/A-Z_0-9]*$', username):
            raise serializers.ValidationError("Symbol")

        if not first_name.isalpha():
            raise serializers.ValidationError("only a-z")


        if not first_name.isalpha():
            raise serializers.ValidationError("only a-z")

        if password!= re_password:
            raise serializers.ValidationError("only a-z")

        try:
            validate_password(password)
        except serializers.ValidationError as err:
            raise serializers.ValidationError(err.messages)

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)          #создание хэшированного пароля
        user.save()
        return user

