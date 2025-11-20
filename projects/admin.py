from django.contrib import admin, messages

from choices.task_statuses import Statuses
from projects.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title",
                    "project",
                    "status",
                    "priority",
                    "assignee",
                    "created_by",
                    "due_date",
                    "estimated_hours",
                    "created_at" )

    list_filter = ("status",
                   "priority",
                   "project",
                   "created_at",
                   "due_date",
                   "assignee",
                   "created_by"
        )

    search_fields = ("title",
                     "description",
                     "project__name"
    )

    ordering = ("-created_at",)
    list_per_page = 25
    list_editable = ("status",
                     "priority",
                     "assignee"
    )
    readonly_fields = ("created_at",
                       "updated_at",
                       "deleted_at"
    )

    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "project")}),
        ("Status & Priority", {"fields": ("status", "priority")}),
        ("Assignment", {"fields": ("assignee", "created_by", "tags")}),
        ("Timeline", {"fields": ("due_date", "estimated_hours")}),
        ("System Fields", {"fields": ("created_at", "updated_at", "deleted_at"), "classes": ("collapse",)}),
    )

actions = ['mark_as_blocked']

@admin.action(description="Перевести задачи в BLOCKED")
def mark_as_blocked(self, request, queryset):
    updated = queryset.update(
        status=Statuses.BLOCKED
    )

    return self.message_user(
        request,
        "Successfully set 'BLOCKED' status for {} tasks".format(updated),
        messages.SUCCESS
    )
