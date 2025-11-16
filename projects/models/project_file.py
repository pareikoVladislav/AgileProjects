from django.db import models

from projects.models.base import BaseFieldsModel


class ProjectFile(BaseFieldsModel):
    name = models.CharField(max_length=120)
    file_path = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files'
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "project_files"
        verbose_name = "Project File"
        verbose_name_plural = "Project Files"
