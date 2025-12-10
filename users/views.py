from rest_framework.generics import ListAPIView, CreateAPIView

from users.models import User
from users.serializers import UserListSerializer, RegisterUserSerializer


# 1.Создайте сериализатор UserListSerialzier для отображения только лишь некоторых полей для пользователя:
# first_name
# last_name
# position
# email
# phone
# last_login
# 1.Создайте классовое отображение UserListGenericView для получения списка пользователей.
# 2.Переопределите метод get_queryset для получения списка пользователей по конкретному проекту, если фильтр был передан, иначе должен отдаваться список всех пользователей.
# 3.Зарегистрируйте новый эндпоинт, протестируйте его, чтобы убедиться, что он работает.
# 4.Закомментируйте все изменения, создайте запрос на слияние.

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


