from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from Art.serializers import ArtworkSerializer
from UserAdministration.serialiazers import UserSerializer, UserProfileSerializer
from Art.models import Artwork, ArtCollection
from Art.serializers import ArtworkSerializer, ArtCollectionViewOnlySerializer
from django.contrib.auth.models import User
from UserFollowWatchApp.models import UserToUserModel
from ArtworkLikeSaveApp.models import UserToArtworkModel
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class MainFeedView(ListAPIView):
    serializer_class = ArtworkSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user).order_by('created_at')


class UserDetailApiView(APIView):
    authentication_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        if request.user:
            data = UserProfileSerializer(request.user.profile, context={'request': request}).data
            return Response(data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileDetailApiView(APIView):
    authentication_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        data={}
        if request.data:
            id = request.data.pop('id', None)
            username = request.data.pop('username', None)
            try:
                if username and id:
                    user = User.objects.get(pk=id, username=username)
                    data['user']=UserProfileSerializer(user.profile, context={'request': request}).data

                    data["like_count"] = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE,
                                                                           artwork__user=user).count()
                    data["follow_count"] = UserToUserModel.objects.filter(activity_type=UserToUserModel.FOLLOW,
                                                                          user=user).count()

                    recent_uploads = Artwork.objects.filter(user=user).order_by('created_at')[:10]
                    data["recent_uploads"]=ArtworkSerializer(recent_uploads, many=True, context={'request': request}).data

                    collection_objs = ArtCollection.objects.filter(user=user).order_by('last_updated_at')[:10]
                    data["collections"] = ArtCollectionViewOnlySerializer(collection_objs, many=True, context={'request': request}).data

                    return Response(data)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except AttributeError or ObjectDoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProfilePlusRecentUploadView(ListAPIView):
    pass


class ProfilePlusCollectionView(ListAPIView):
    pass
