from rest_framework import serializers
from projects.models import Project



class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'date_started',
            'count_of_files',
        ]