from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveDestroyAPIView

from projects.models import ProjectFile, Project
from projects.serializers.project_file import (
    AllProjectFilesSerializer,
    CreateProjectFileSerializer,
    ProjectFileDetailSerializer,
)
from utils import delete_file


class ProjectFileListGenericView(ListCreateAPIView):
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return AllProjectFilesSerializer

        elif self.request.method == 'POST':
            return CreateProjectFileSerializer

    def get_queryset(self):
        qs = ProjectFile.objects.all()

        project_name = self.request.query_params.get('project')

        if project_name:
            # proj = Project.objects.get(name=project_name)
            qs = qs.filter(
                projects__name=project_name
            )

        return qs

    def create(self, request: Request, *args, **kwargs) -> Response:
        file_content = request.FILES["file"]
        project_id = request.data["project_id"]
        request.data['file_name'] = file_content.name if file_content else None

        project = get_object_or_404(Project, pk=project_id)

        serializer = self.get_serializer(
            data=request.data,
            context={
                "raw_file": file_content,
                "project": project
            }
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                data={
                    "message": "File upload successfully"
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectFileDetailGenericView(RetrieveDestroyAPIView):
    serializer_class = ProjectFileDetailSerializer
    queryset = ProjectFile.objects.all()

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            delete_file(obj.file_path)
            obj.delete()
            return Response(
                data={},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as exc:
            return Response(
                data=str(exc),
                status=status.HTTP_400_BAD_REQUEST
            )
