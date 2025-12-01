from django.contrib import admin
from .models import Project, Task, Tag
# from django.template.library import TagHelperNode


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'projects', 'status', 'priority', 'created_at', 'due_date')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)



'''Настройте отображение моделей Project, Task, Tag в админ-панели. Реализуйте следующие возможности:
Поиск по названию задачи для модели Task. 
Поиск по названию проекта для модели Project.
У модели Task в Админ-панели должны отображаться поля:
Название задачи
Проект
Статус
Приоритетность
Дата создания
Дата сдачи задачи (due_date)'''




