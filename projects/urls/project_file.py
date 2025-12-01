from django.urls import path

from projects.views.project_file import ProjectFileListGenericView


urlpatterns = [
    path('', ProjectFileListGenericView.as_view()),
]
