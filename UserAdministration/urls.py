from rest_framework.routers import DefaultRouter
from UserAdministration.views import ProfileViewSet, UserViewSet, AddressViewSet

user_admin_router=DefaultRouter()
user_admin_router.register('profile', ProfileViewSet, base_name='profile')
user_admin_router.register('user', UserViewSet, base_name='user')
user_admin_router.register('address', AddressViewSet, base_name='address')
