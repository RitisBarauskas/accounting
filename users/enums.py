import enum


class UserRolesEnum(enum.Enum):
    """
    Роли пользователей.
    """
    ADMIN = 'Администратор'
    AUTHOR = 'Автор'

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)

    @classmethod
    def choices_role(cls):
        return tuple(item.name for item in cls)
