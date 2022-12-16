from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer, IntegerField

from teasers.models import Teaser
from teasers.enums import TeaserStatusEnum


class TeaserAdminSerializer(ModelSerializer):
    class Meta:
        model = Teaser
        fields = ('id', 'title', 'description', 'category', 'status', 'author', 'price')
        read_only_fields = ('id','price', 'author')

    def validate(self, attrs):
        if self.instance.status != TeaserStatusEnum.NEW.name:
            raise ValidationError(
                f'Невозможно изменить данные тизера, который имеет статус отличный от {TeaserStatusEnum.NEW.value}'
            )

        return super().validate(attrs)


class TeaserListCreateUpdateSerializer(ModelSerializer):
    """
    Сериализатор создания тизеров.
    """

    class Meta:
        model = Teaser
        fields = ('id', 'title', 'description', 'category', 'author', 'price', 'status')
        read_only_fields = ('id', 'price', 'author', 'status')

    def validate(self, attrs):
        if self.context.get('request').method != 'POST' and self.instance.status != TeaserStatusEnum.NEW.name:
            raise ValidationError(
                f'Невозможно изменить данные тизера, который имеет статус отличный от {TeaserStatusEnum.NEW.value}'
            )

        return super().validate(attrs)


class WalletSerializer(Serializer):
    """
    Сериализатор кошелька.
    """
    amount = IntegerField()
