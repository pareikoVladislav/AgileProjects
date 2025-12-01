# Напишите сериализатор для работы с тегами (так как у нас всего одно поле в этой модели,
# сериализатор будет один на все будущие запросы).

from rest_framework import serializers
from projects.models import Tag



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"