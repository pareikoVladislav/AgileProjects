from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    files = models.ManyToManyField(
        'ProjectFile',
        related_name='projects',
        blank=True
    )
    date_started = models.DateField(auto_now_add=True)

    @property
    def count_of_files(self):
        return self.files.count()

    class Meta:
        db_table = "projects"
        ordering = ['-name']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name
