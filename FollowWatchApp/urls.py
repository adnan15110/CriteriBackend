from rest_framework.routers import DefaultRouter
from FollowWatchApp.views import FollowerModelViewSet, WatcherModelViewSet

user_preference_router=DefaultRouter()
user_preference_router.register('follow', FollowerModelViewSet, base_name='user-follow')
user_preference_router.register('watch', WatcherModelViewSet, base_name='user-watch')