from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from choices.task_statuses import Statuses, Priority
from projects.models import Project, BaseFieldsModel


class Task(BaseFieldsModel):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(10)]
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=Statuses.choices(),
        default=Statuses.NEW
    )
    priority = models.CharField(
        max_length=15,
        choices=Priority.choices(),
        default=Priority.MEDIUM
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="subtasks"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignee = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='tasks'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = ['project', 'title']
