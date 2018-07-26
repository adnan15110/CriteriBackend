from rest_framework.routers import DefaultRouter
from UserAdministration.views import UserProfileViewSet, UserViewSet

user_admin_router=DefaultRouter()
user_admin_router.register('profile', UserProfileViewSet)
user_admin_router.register('user', UserViewSet)
