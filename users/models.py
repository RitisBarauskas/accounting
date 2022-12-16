from django.contrib.auth.models import AbstractUser
from django.db import models

from users.enums import UserRolesEnum


class UserAccounting(AbstractUser):
    """
    Пользователь системы.
    """
    role = models.CharField(
        verbose_name='Роль',
        choices=UserRolesEnum.choices(),
        default=UserRolesEnum.AUTHOR.name,
        max_length=50,
    )

    @property
    def is_author(self):
        return self.role == UserRolesEnum.AUTHOR.name

    @property
    def is_admin(self):
        return (
            self.role == UserRolesEnum.ADMIN.name
            or self.is_staff
            or self.is_superuser
        )
