from django.core.validators import MinLengthValidator
from django.db import models

'''Создайте модель Project со следующими полями:
Название проекта: строковое, уникальное
Описание проекта: строковое, большое поле, обязательно к заполнению
Дата создания проекта: должна проставляться автоматически при создании'''

from django.db import models

class Project(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True)

'''Создайте модель Task со следующими полями:
Название задачи: строковое поле, уникальное, минимальная длина названия - 10 символов
Описание: большое строковое поле, может быть пустым
Статус: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных статусов. По умолчанию все задачи новые
Приоритет: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных приоритетов
Проект: связь с моделью Project, при удалении проекта все задачи должны удаляться
Дата создания задачи: поле, поддерживающее и дату, и время, заполняется автоматически только при создании
Дата обновления: поле, поддерживающее и дату, и время, заполняется автоматически всегда
Дата удаления: поле, в котором может ничего не быть'''


list_status = [
    ('new', 'Новая'),
    ('in_progress', 'В процессе'),
    ('bloked', 'Заблокирована'),
    ('pending', 'Приостановлена'),
    ('testing', 'Тестирование'),
    ('inreview', 'На проверке'),
    ('done', 'Завершено')
    ]

list_priority = [
    ('3', 'Высокий'),
    ('2', 'Средний'),
    ('1', 'Низкий'),
]

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(10)])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=list_status, default='new')
    priority = models.CharField(max_length=15, choices=list_priority)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.priority}"


'''Расширьте модель Task дополнительным хранением тегов:
Создайте модель тегов (Tag):
Имя тэга (Строковое поле, уникальное)
Добавьте поле due_date (срок выполнения) в модель Task.
Свяжите модель Задачи с тегами через связь “Многие ко многим”, добавив в модель задачи новое поле tags'''

class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='childs', null=True, blank=True)  # todo: manytomany связи тегов!


    def __str__(self):
        return self.name






