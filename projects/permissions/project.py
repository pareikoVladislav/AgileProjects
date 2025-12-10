from rest_framework.permissions import BasePermission

from projects.models import Project


class CanViewProjectTasks(BasePermission):

    def has_permission(self, request, view):
        #print('+' * 100)
        #print(view.kwargs['pk'])
        #print('+'*100)
        if request.user and request.user.is_authenticated:
            #if request.user.current_project_id == view.kwargs['pk']:
            obj = Project.objects.get(pk=view.kwargs['pk'])
            if request.user.current_project == obj:
                return True
        return False


