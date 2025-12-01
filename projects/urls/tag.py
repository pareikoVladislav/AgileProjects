from django.urls import path

from projects.views.tag import TagListAPIView, TagDetailAPIView


urlpatterns = [
    path('', TagListAPIView.as_view()),
    path('<int:pk>/', TagDetailAPIView.as_view())
]
