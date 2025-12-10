from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.models import Task
from projects.models import Project
from projects.permissions.project import CanViewProjectTasks
from projects.serializers import AllTasksSerializer
from projects.serializers.project import ProjectDetailSerializer, CreateProjectSerializer, AllProjectsSerializer


# Задание 1. Custom permission: доступ к задачам только участникам проекта
# ### Эндпоинты:
# - GET /api/v1/projects/<project_id>/tasks/
# - POST /api/v1/projects/<project_id>/tasks/
# - GET/PUT/DELETE /api/v1/projects/<project_id>/tasks/<id>/
#
# ### Требования
# - Реализовать custom permission, который:
#   - Разрешает доступ только пользователям, у которых:
#     - либо `current_project` = project_id,
#     - либо пользователь связан с этим проектом через ManyToMany `projects`.
#   - Для администраторов (`is_staff=True`) доступ всегда разрешён.
# - Подключить этот permission ко всем указанным эндпоинтам.
# - При нарушении прав возвращать 403 с понятным сообщением об ошибке.




class ProjectsListAPIView(APIView):
   def get_objects(self, date_from=None, date_to=None):
       if date_from and date_to:
           date_from = timezone.make_aware(
               datetime.strptime(date_from, '%Y-%m-%d')
           )
           date_to = timezone.make_aware(
               datetime.strptime(date_to, '%Y-%m-%d')
           ) if date_from else timezone.now().strftime('%Y-%m-%d')

           projects = Project.objects.filter(
               created_at__range=[date_from, date_to]
           )

           return projects

       return Project.objects.all()

   def get(self, request: Request) -> Response:
       date_from = request.query_params.get('date_from')
       date_to = request.query_params.get('date_to')

       projects = self.get_objects(date_from, date_to)

       if not projects.exists():
           return Response(
               data=[],
               status=status.HTTP_204_NO_CONTENT
           )

       serializer = AllProjectsSerializer(projects, many=True)

       return Response(
           serializer.data,
           status=status.HTTP_200_OK,
       )

   def post(self, request: Request) -> Response:
       serializer = CreateProjectSerializer(data=request.data)

       if serializer.is_valid(raise_exception=True):
           serializer.save()

           return Response(
               serializer.validated_data,
               status=status.HTTP_201_CREATED,
           )

       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST,
       )


class ProjectDetailAPIView(APIView):
   def get_object(self, pk: int):
       return get_object_or_404(Project, pk=pk)

   def get(self, request: Request, pk: int) -> Response:
       project = self.get_object(pk=pk)

       serializer = ProjectDetailSerializer(project)

       return Response(
           serializer.data,
           status=status.HTTP_200_OK,
       )

   def put(self, request, pk: int):

       project = self.get_object(pk=pk)

       serializer = CreateProjectSerializer(
           instance=project,
           data=request.data,
           partial=True
       )
       if serializer.is_valid(raise_exception=True):
           serializer.save()

           return Response(
               serializer.validated_data,
               status=status.HTTP_200_OK,
           )

       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST,
       )

class ProjectTasksAPIView(ListCreateAPIView):
    serializer_class = AllTasksSerializer
    permission_classes = [CanViewProjectTasks]

    def get_queryset(self):
        return Task.objects.filter(project=self.kwargs['pk'])


