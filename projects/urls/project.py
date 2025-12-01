from django.urls import path

from projects.views.project import ProjectsListAPIView, ProjectDetailAPIView

urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
]
