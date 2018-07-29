from rest_framework.routers import DefaultRouter
from Art.views import ArtCategoryViewSet, ArtworkViewSet, ArtCollectionViewSet

art_router=DefaultRouter()
art_router.register('artwork', ArtworkViewSet, base_name='artwork')
art_router.register('art-category', ArtCategoryViewSet, base_name='art-category')
art_router.register('art-collection', ArtCollectionViewSet, base_name='art-collection')
