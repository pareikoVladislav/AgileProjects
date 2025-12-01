from django.urls import path, include


urlpatterns = [
    path('tags/', include('projects.urls.tag')),
    path('tasks/', include('projects.urls.task')),
    path('projects/', include('projects.urls.project')),
    path('project_files/', include('projects.urls.project_file')),
    path('users/', include('users.urls')),
]
