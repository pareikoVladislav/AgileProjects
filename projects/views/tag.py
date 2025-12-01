from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from projects.models import Tag
from projects.serializers.tag import TagSerializer


class TagListAPIView(APIView):

    def get_queryset(self) -> QuerySet[Tag, Tag]:
        return Tag.objects.all()

    def get(self, request: Request) -> Response:
       tags = self.get_queryset()

       if not tags.exists():
           return Response(
               data=[],
               status=status.HTTP_204_NO_CONTENT
           )

       serializer = TagSerializer(tags, many=True)

       return Response(
           data=serializer.data,
           status=status.HTTP_200_OK
       )

    def post(self, request: Request) -> Response:

        serializer = TagSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class TagDetailAPIView(APIView):
   def get_object(self, pk: int) -> Tag:
       return get_object_or_404(Tag, pk=pk)

   def get(self, request: Request, pk: int) -> Response:
       tag = self.get_object(pk=pk)

       serializer = TagSerializer(tag)

       return Response(
           serializer.data,
           status=status.HTTP_200_OK,
       )

   def put(self, request: Request, pk: int) -> Response:
       tag = self.get_object(pk=pk)

       serializer = TagSerializer(tag, data=request.data)

       if serializer.is_valid(raise_exception=True):
           serializer.save()

           return Response(
               serializer.validated_data,
               status=status.HTTP_200_OK,
           )

       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )

   def delete(self, request: Request, pk: int) -> Response:
       tag = self.get_object(pk=pk)

       tag.delete()

       return Response(
           data={"message": "Tag was deleted successfully"},
           status=status.HTTP_200_OK
       )
