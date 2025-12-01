from django.urls import path

from projects.views.project_file import (
    ProjectFileListGenericView,
    ProjectFileDetailGenericView)

urlpatterns = [
    path('', ProjectFileListGenericView.as_view()),
    path('<int:pk>', ProjectFileDetailGenericView.as_view()),
]
