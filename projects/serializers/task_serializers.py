from datetime import datetime
from typing import Any

from rest_framework import serializers
from projects.models import Task, Project, Tag
from django.utils import timezone

from projects.serializers.project import ProjectShortInfoSerializer
from projects.serializers.tag import TagSerializer


class TaskDetailSerializer(serializers.ModelSerializer):
   project = ProjectShortInfoSerializer()
   tags = TagSerializer(many=True, read_only=True)

   class Meta:
       model = Task
       exclude = ('updated_at', 'deleted_at')


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field="name", # используем только на уникальные колонки
        read_only="True"
    )

    assignee = serializers.SlugRelatedField(
        slug_field="email",
        read_only="True"
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "status",
            "priority",
            "project",
            "assignee",
            "due_date"
        ]

class CreateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Project.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "priority",
            "project",
            "tags",
            "due_date"
        ]

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Минимальная длина названия задачи должна быть больше 10")
        return value

    def validate_description(self, value):
        if len(value) < 50:
            raise serializers.ValidationError("Минимальная длина описания задачи должна быть больше 50")
        return value

    def validate_project_name(self, value):
        if not Project.objects.filter(name=value):
            raise serializers.ValidationError("Такого названия проекта не существует!")
        return value

    def validate_tags(self, value):
        if not Tag.objects.filter(name__in=value):
            raise serializers.ValidationError("Такого тэга не существует!")
        return value

    def validate_due_date(self, value):
        time_data = datetime.strptime(
            datetime.strftime(value, "%Y-%m-%dT%H:%M:%S"),
            "%Y-%m-%dT%H:%M:%S"
        )
        value = timezone.make_aware(time_data, timezone.get_current_timezone())
        if value < timezone.now():
            raise serializers.ValidationError("Deadline не может существовать в прошлом!")
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])

        task = Task.objects.create(**validated_data)

        for tag in tags:
            task.tags.add(tag)

        task.save()
        return task

    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags:
            for tag in tags:
                instance.tags.add(tag)

        instance.save()

        return instance
