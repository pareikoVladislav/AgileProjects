from django.urls import path

from projects.views.task import TasksListAPIView, TaskDetailAPIView


urlpatterns = [
    path('', TasksListAPIView.as_view()),
    path('<int:pk>/', TaskDetailAPIView.as_view()),
]
