import datetime

from django.db.models import Q, Sum
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK

from teasers.enums import TeaserStatusEnum
from teasers.models import Teaser, Price
from api.serializers import TeaserSerializer, TeaserCreateUpdateSerializer, WalletSerializer
from api.permissions import IsAdmin, IsAuthor


class TeaserAuthorViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,

):
    """
    Вьюсет тизеров.
    """
    serializer_class = TeaserCreateUpdateSerializer
    permission_classes = [IsAuthor,]

    def get_queryset(self):
        return Teaser.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        price = Price.objects.filter(
            (Q(end__gt=datetime.date.today()) | Q(end__isnull=True)),
            start__lte=datetime.date.today(),
        ).first()

        serializer.save(price=price, author=self.request.user)

    @action(methods=['GET',], detail=False, permission_classes=(IsAuthor,))
    def wallet(self, request):
        amount = request.user.teasers.filter(
            status=TeaserStatusEnum.APPROVED.name
        ).aggregate(
            amount=Sum('price__amount'),
        )
        serializer = WalletSerializer(amount)

        return Response(serializer.data, status=HTTP_200_OK)


class TeaserAdminViewSet(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    Вьюсет тизеров.
    """
    serializer_class = TeaserSerializer
    permission_classes = [IsAdmin,]
    queryset = Teaser.objects.all()
