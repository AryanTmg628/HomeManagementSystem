from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DoorLockViewSet

router = DefaultRouter()
router.register(r"", DoorLockViewSet, basename="door-lock")

urlpatterns = router.urls
