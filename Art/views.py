from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from Art.serializers import ArtCategorySerializer, ArtworkSerializer, ArtCollectionSerializer
from Art.models import Artwork, ArtCategory, ArtCollection
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class ArtCategoryViewSet(ModelViewSet):
    serializer_class = ArtCategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return ArtCategory.objects.all()


class ArtworkViewSet(ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (MultiPartParser, JSONParser)

    @action(methods=['post'], detail=True)
    def add_to_categories(self, request, pk=None):
        artwork = self.get_object()
        categories = self.request.data
        for category in categories:
            try:
                obj = ArtCategory.objects.get(id=category['id'], category_name=category['category_name'])
                artwork.categories.add(obj)
            except ObjectDoesNotExist:
                pass
        return Response({'added'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def delete_from_categories(self, request, pk=None):
        artwork = self.get_object()
        categories = self.request.data
        for category in categories:
            try:
                obj = ArtCategory.objects.get(id=category['id'], category_name=category['category_name'])
                artwork.categories.remove(obj)
            except ObjectDoesNotExist:
                pass
        return Response({'removed'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ArtCollectionViewSet(ModelViewSet):
    queryset = ArtCollection.objects.all()
    serializer_class = ArtCollectionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (JSONParser,)

    @action(methods=['post'], detail=True)
    def add_to_collection(self, request, pk=None):
        Collection = self.get_object()
        artworks_list = self.request.data
        for art in artworks_list:
            try:
                obj = Artwork.objects.get(id=art['id'], title=art['title'])
                Collection.artworks.add(obj)
            except ObjectDoesNotExist:
                pass
        return Response({'added'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def delete_from_collection(self, request, pk=None):
        Collection = self.get_object()
        artworks_list = self.request.data
        for art in artworks_list:
            try:
                obj = Artwork.objects.get(id=art['id'], title=art['title'])
                Collection.artworks.remove(obj)
            except ObjectDoesNotExist:
                pass
        return Response({'removed'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)