from django.urls import path

from projects.views.project import (
    ProjectsListAPIView,
    ProjectDetailAPIView,
    ProjectTasksAPIView,
)

urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('<int:pk>/tasks/', ProjectTasksAPIView.as_view())
]
