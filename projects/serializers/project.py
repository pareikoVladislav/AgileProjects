from rest_framework import serializers

from projects.models import Project


class ProjectShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ProjectDetailSerializer(serializers.ModelSerializer):

   class Meta:
       model = Project
       fields = ('id', 'name', 'description', 'count_of_files')


class AllProjectsSerializer(serializers.ModelSerializer):

   class Meta:
       model = Project
       fields = ('id', 'name', 'date_started')


class CreateProjectSerializer(serializers.ModelSerializer):
   date_started = serializers.DateTimeField(read_only=True)

   class Meta:
       model = Project
       fields = ('name', 'description', 'date_started')

   def validate_description(self, value: str) -> str:
       if len(value) < 30:
           raise serializers.ValidationError(
               "Description must be at least 30 characters long"
           )

       return value
