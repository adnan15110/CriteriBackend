from rest_framework import routers
from criteri.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)