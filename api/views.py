import datetime

from django.db.models import Q, Sum
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK

from teasers.enums import TeaserStatusEnum
from teasers.models import Teaser, Price
from api.serializers import TeaserAdminSerializer, TeaserListCreateUpdateSerializer, WalletSerializer
from api.permissions import IsAdmin, IsAuthor


class TeaserViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,

):
    """
    Вьюсет тизеров.
    """
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        if self.request.user.is_admin:
            return Teaser.objects.all()

        return self.request.user.teasers.all()

    def get_permissions(self):
        if self.request.user.is_admin:
            permission_classes = (IsAdmin,)
        else:
            permission_classes = (IsAuthor,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return TeaserAdminSerializer

        return TeaserListCreateUpdateSerializer

    def perform_create(self, serializer):
        price = Price.objects.filter(
            (Q(end__gt=datetime.date.today()) | Q(end__isnull=True)),
            start__lte=datetime.date.today(),
        ).first()

        serializer.save(price=price, author=self.request.user)

    @action(methods=('GET',), detail=False, permission_classes=(IsAuthor,))
    def wallet(self, request):
        amount = request.user.teasers.filter(
            status=TeaserStatusEnum.APPROVED.name
        ).aggregate(
            amount=Sum('price__amount'),
        )
        serializer = WalletSerializer(amount)

        return Response(serializer.data, status=HTTP_200_OK)
