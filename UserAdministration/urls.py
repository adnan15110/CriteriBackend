from rest_framework.routers import DefaultRouter
from UserAdministration.views import ProfileViewSet, UserViewSet, AddressViewSet

user_admin_router=DefaultRouter()
user_admin_router.register('profile', ProfileViewSet)
user_admin_router.register('user', UserViewSet)
user_admin_router.register('address', AddressViewSet)
