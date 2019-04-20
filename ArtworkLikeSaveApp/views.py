from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from ArtworkLikeSaveApp.serializers import ArtworkLikeSerializer, ArtworkSaveSerializer
from ArtworkLikeSaveApp.models import UserToArtworkModel
from Art.models import Artwork
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# Create your views here.


class ArtworkLikeModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
        list:
            Return a list of images liked by the logged user.

        create:
            Create a artwork like relation for logged user to the selected artwork.
            params:
            {
            'artwork_id': number,
            'artwork_title': string,
            }
    """
    serializer_class = ArtworkLikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (JSONParser, FormParser)

    def get_queryset(self):
        return UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE)

    @action(detail=False)
    def artwork_like_count(self, request):
        """
        returns the like count of logged user's artwork
        """
        total = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE,
                                                  artwork__user=request.user).count()
        return Response({'likes': total})

    @action(detail=False)
    def user_like_count(self, request):
        """
        returns the like count by user
        """
        total = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE, user=request.user).count()
        return Response({'likes': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        """
        removes the artwork like request.
        :param:
            {
            'artwork_id': number,
            'artwork_title': string,
            }
        :return:
        """
        artwork_id = request.data.pop('artwork_id', None)
        artwork_title = request.data.pop('artwork_title', None)

        try:
            if artwork_id and artwork_title:
                artwork = Artwork.objects.get(pk=artwork_id, title=artwork_title)
                objs = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE,
                                                         user=request.user,
                                                         artwork=artwork)
            if objs:
                objs.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ArtworkSaveModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    list:
        Return a list of images saved by the logged user.

    create:
        Create a artwork save relation for logged user to the selected artwork.
        params:
        {
        'artwork_id': number,
        'artwork_title': string,
        }
    """
    serializer_class = ArtworkSaveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.SAVE, user=self.request.user)

    @action(detail=False)
    def save_count(self, request):
        """
        returns count of images saved by the logged user.
        :param request: None
        :return: {'count': number}
        """
        total = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.SAVE, user=request.user).count()
        return Response({'count': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        """
        returns count of images saved by the logged user.
        :param request:
        {
        'artwork_id': number,
        'artwork_title': string,
        }
        :return: None

        """
        artwork_id = request.data.pop('artwork_id', None)
        artwork_title = request.data.pop('artwork_title', None)

        try:
            if artwork_id and artwork_title:
                artwork = Artwork.objects.get(pk=artwork_id, title=artwork_title)
                objs = UserToArtworkModel.objects.get(activity_type=UserToArtworkModel.SAVE,
                                                      user=request.user,
                                                      artwork=artwork)
            if objs:
                objs.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)
