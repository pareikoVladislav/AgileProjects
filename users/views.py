from rest_framework.generics import ListAPIView, CreateAPIView
from users.serializers import UserListSerializer, RegisterUserSerializer
from users.models import User

class UserListGenericView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        project_filter = self.request.query_params.get('project')
        if project_filter:
            queryset = queryset.filter(current_project__name=project_filter)

        return queryset

class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()



