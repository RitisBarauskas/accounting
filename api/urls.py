from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TeaserViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'teasers',
    TeaserViewSet,
    basename='teasers',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
