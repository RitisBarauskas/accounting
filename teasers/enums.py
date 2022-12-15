import enum


class TeaserStatusEnum(enum.Enum):
    """
    Статусы тизеров.
    """
    NEW = 'Новая'
    REJECTED = 'Отклонена'
    APPROVED = 'Оплачена'

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)

    @classmethod
    def choices_status(cls):
        return tuple(item.name for item in cls)
