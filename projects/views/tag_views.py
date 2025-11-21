from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from projects.models import Tag
from projects.serializers import TagSerializer



class TagListCreateAPIView(APIView):
    def get(self, request: Request):
        tags = Tag.objects.all()
        response = TagSerializer(tags, many=True)

        return Response(data=response.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        raw_data = request.data
        data = TagSerializer(data=raw_data)
        if data.is_valid():
            data.save()
            return Response(data=data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailApiView(APIView):

    def get_object(self, pk: int):
        try:
            tag=Tag.objects.get(id=pk)
            return tag
        except Tag.DoesNotExist:
            raise Tag.DoesNotExist


    def get(self, request: Request, pk: int):
        try:
            tag = self.get_object(pk)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": f"Тег с id {pk} не найден "
                },
                status=status.HTTP_404_NOT_FOUND
            )
        response = TagSerializer(tag)
        return Response (data=response.data, status=status.HTTP_200_OK)


    def put(self, request: Request, pk: int):
        try:
            tag = self.get_object(pk)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": f"Тег с id {pk} не найден "
                },
                status=status.HTTP_404_NOT_FOUND
            )
        new_tag = TagSerializer(instance=tag, data=request.data)

        if not new_tag.is_valid():
            return Response(data=new_tag.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            new_tag.save()
            return Response(data=new_tag.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int):
        try:
            tag = self.get_object(pk)
            tag.delete()
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response(
                data={
                    "message": f"Тег с id {pk} не найден "
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as err:
            return Response(data=str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



