"""
Devices app URL routing.
"""
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DeviceViewSet, NodeViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"devices",    DeviceViewSet,   basename="device")
router.register(r"nodes",      NodeViewSet,     basename="node")

urlpatterns = router.urls
