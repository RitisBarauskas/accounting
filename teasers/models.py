import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from teasers.enums import TeaserStatusEnum

User = get_user_model()


class Price(models.Model):
    """
    Цена тизера.
    """
    amount = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    start = models.DateField(
        verbose_name='Дата начала действия',
    )
    end = models.DateField(
        verbose_name='Дата окончания действия',
    )
    current = models.BooleanField(
        verbose_name='Последняя версия',
        default=True,
    )

    class Meta:
        verbose_name='Стоимость тизера'
        verbose_name_plural='Цены тизеров'
        ordering=('-end',)

    def __str__(self):
        return f'Цена {self.amount} действует с {self.start} до {self.end}'

    def clean(self):
        if self.end < self.start:
            raise ValidationError({'start': 'Дата начала действия цены не может быть больше даты окончания.'})
        if self.start < datetime.date.today():
            raise ValidationError({'start': 'Стоимость нельзя менять задним числом'})

        old_price = self._meta.model.objects.filter(current=True).order_by('-start').first()
        if old_price:
            if self.start <= old_price.start:
                raise ValidationError(
                    {'start': f'Дата начала не должна быть меньше даты начала предыдущей цены ({old_price.start})'},
                )
            old_price.end = self.start
            old_price.current = False
            old_price.save()

        super().clean()


class Category(models.Model):
    """
    Категория тизера.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=64,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание категории',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    active = models.BooleanField(
        verbose_name='Статус',
        default=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Teaser(models.Model):
    """
    Тизер.
    """
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=64,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='teasers',
        verbose_name='Категория',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='teasers',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=50,
        choices=TeaserStatusEnum.choices(),
        default=TeaserStatusEnum.NEW,
        verbose_name='Статус',
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.PROTECT,
        related_name='teasers',
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'Тизер'
        verbose_name_plural = 'Тизеры'
        ordering = ('-created_at',)

    def __str__(self):
        name = self.author.get_full_name() if self.author.get_full_name() else self.author.username

        return f'{self.title} от {name}'

    def clean(self):
        if self.status != TeaserStatusEnum.NEW:
            raise ValidationError(
                {'status': f'Нельзя менять тизеры, которые имеют отличный статус от "{TeaserStatusEnum.NEW.value}"'},
            )

