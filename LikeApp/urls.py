from rest_framework.routers import DefaultRouter
from LikeApp.views import UserToUserModelLikeViewSet, UserToUserModelSaveViewSet

user_preference_router=DefaultRouter()
user_preference_router.register('likes', UserToUserModelLikeViewSet, base_name='user-like')
user_preference_router.register('saves', UserToUserModelSaveViewSet, base_name='user-save')