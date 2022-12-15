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
        default=UserRolesEnum.AUTHOR,
        max_length=50,
    )
