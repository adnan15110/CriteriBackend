from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from Art.serializers import ArtCategorySerializer, ArtworkSerializer, ArtCollectionSerializer
from Art.models import Artwork, ArtCategory, ArtCollection
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class ArtCategoryViewSet(ModelViewSet):
    """
        retrieve:
            Return the given art category.

        list:
            Return a list of available art category.

        create:
            Create an art category .

        update:
            Updates an existing art category.

        partial_update:
            Partially updates an existing art category.

        delete:
            Deletes an existing art category.
    """
    serializer_class = ArtCategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (JSONParser, FormParser)

    def get_queryset(self):
        return ArtCategory.objects.all()


class ArtworkViewSet(ModelViewSet):
    """
        retrieve:
            Return the given artwork.

        list:
            Return a list of available artwork.

        create:
            Create an artwork. This is not a json request. you need to use form request as the data has an image to upload.

        update:
            Updates an existing artwork.

        partial_update:
            Partially updates an existing artwork.

        delete:
            Deletes an existing artwork.
    """
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (MultiPartParser, JSONParser)

    @action(methods=['post'], detail=True)
    def add_to_categories(self, request, pk=None):
        """
        Adds art categories to from artwork art categories.
        example post data:
        category_data = [
            {
                "id": 1,
                "category_name": 'NAME'
            },
            {
                "id": 2,
                "category_name": 'NAME'
            },
            {
                "id": 3,
                "category_name": 'NAME'
            },
        ]

        :param request: list of art category e.g., [{'id':2, 'category_name': 'oil painting'}]
        :param pk: Not required
        :return: http 200 on success.
        """
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
        """
        deletes art categories to from artwork art categories.
        :param request: list of art category e.g., [{'id':2, 'category_name': 'oil painting'}]
        :param pk: Not required
        :return: http 200 on success.
        """
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
    """
        retrieve:
            Return the given collection with list of artworks

        list:
            Return a list of available artwork collections.

        create:
            Create an artwork collection.

        update:
            Updates an existing artwork collection.

        partial_update:
            Partially updates an existing collection.

        delete:
            Deletes an existing artwork collection.
    """
    queryset = ArtCollection.objects.all()
    serializer_class = ArtCollectionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (JSONParser,)

    @action(methods=['post'], detail=True)
    def add_to_collection(self, request, pk=None):
        """
        adds a list of artwork to the collection. Please disregard the auto generated json in the
        api docs. the request accepts list of artworks in the following format.
        :param request: = [
            {
                "id": artwork.id,
                "title": 'artwork.title'
            },
            {
                "id": artwork.id,
                "title": 'artwork.title'
            }
        ]
        :param pk:
        :return: 200
        """
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
        """
        deletes a list of artwork from the collection (params are same as the add to collection request)
        :param request: = [
            {
                "id": artwork.id,
                "title": 'artwork.title'
            },
            {
                "id": artwork.id,
                "title": 'artwork.title'
            }
        ]
        :param pk:
        :return: 200
        """
        collection = self.get_object()
        artworks_list = self.request.data
        for art in artworks_list:
            try:
                obj = Artwork.objects.get(id=art['id'], title=art['title'])
                collection.artworks.remove(obj)
            except ObjectDoesNotExist:
                pass
        return Response({'removed'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)