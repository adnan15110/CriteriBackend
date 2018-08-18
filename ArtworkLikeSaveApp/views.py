from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from ArtworkLikeSaveApp.serializers import ArtworkLikeSerializer, ArtworkSaveSerializer
from ArtworkLikeSaveApp.models import UserToArtworkModel
from Art.models import Artwork
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Create your views here.


class ArtworkLikeModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArtworkLikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE)

    @action(detail=False)
    def artwork_like_count(self, request):
        return Response({'likes': 10})

    @action(detail=False)
    def user_like_count(self, request):
        total = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE, user=request.user).count()
        return Response({'likes': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        artwork_id = request.data.pop('artwork_id', None)
        artwork_title = request.data.pop('artwork_title', None)

        try:
            if artwork_id and artwork_title:
                artwork = Artwork.objects.get(pk=artwork_id, title=artwork_title)
                obj = UserToArtworkModel.objects.get(activity_type=UserToArtworkModel.LIKE,
                                                     user=request.user,
                                                     artwork=artwork)
            if obj:
                obj.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ArtworkSaveModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ArtworkSaveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.SAVE)

    @action(detail=False)
    def save_count(self, request):
        total = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.SAVE, user=request.user).count()
        return Response({'count': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        artwork_id = request.data.pop('artwork_id', None)
        artwork_title = request.data.pop('artwork_title', None)

        try:
            if artwork_id and artwork_title:
                artwork = Artwork.objects.get(pk=artwork_id, title=artwork_title)
                obj = UserToArtworkModel.objects.get(activity_type=UserToArtworkModel.SAVE,
                                                     user=request.user,
                                                     artwork=artwork)
            if obj:
                obj.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)
