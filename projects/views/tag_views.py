from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from projects.models import Tag
from projects.serializers import TagSerializer

class TagListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()
        response = TagSerializer(tags, many=True)
        return Response(
            data=response.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        raw_data = request.data
        tag = TagSerializer(data=raw_data)
        if not tag.is_valid():
            return Response(
                data=tag.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            tag.save()
        except Exception as exc:
            return Response(
                data={"error": f"Ошибка при сохранении тэга: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        return Response(
            data=tag.data,
            status=status.HTTP_201_CREATED
            )





