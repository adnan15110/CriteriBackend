from rest_framework.routers import DefaultRouter
from ArtworkLikeSaveApp.views import ArtworkLikeModelViewSet, ArtworkSaveModelViewSet

artwork_preference_router=DefaultRouter()
artwork_preference_router.register('like', ArtworkLikeModelViewSet, base_name='user-like')
artwork_preference_router.register('save', ArtworkSaveModelViewSet, base_name='user-save')