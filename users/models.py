from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from choices.positions import UserPositions


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(
        _("first name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True
    )
    phone = models.CharField(max_length=75, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        name="registered", auto_now_add=True
    )
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    position = models.CharField(
        max_length=25,
        choices=UserPositions.choices(),
        default=UserPositions.BACKEND_DEVELOPER.name
    )
    projects = models.ManyToManyField(
        "projects.Project",
        related_name="users",
    )
    current_project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        related_name="current_members",
        null=True,
        blank=True,
        help_text="Primary project user is currently working on"
    )
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Hourly rate for time tracking"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "position"
    ]

    objects = UserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
