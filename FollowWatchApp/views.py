from rest_framework.viewsets import GenericViewSet
from  rest_framework import status
from rest_framework import mixins
from FollowWatchApp.serializers import UserFollowSerializer, UserWatchSerializer
from FollowWatchApp.models import UserToUserModel
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Create your views here.


class FollowerModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return UserToUserModel.objects.filter(activity_type=UserToUserModel.FOLLOW)

    @action(detail=False)
    def follow_count(self, request):
        total = UserToUserModel.objects.filter(activity_type=UserToUserModel.FOLLOW, base_user=request.user).count()
        return Response({'follower': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        user_id = request.data.pop('user_id', None)
        username = request.data.pop('user_name', None)

        try:
            if user_id:
                user = User.objects.get(pk=user_id)
                obj = UserToUserModel.objects.get(activity_type=UserToUserModel.FOLLOW, base_user=request.user, user=user)
            elif username:
                user = User.objects.get(username=username)
                obj = UserToUserModel.objects.get(activity_type=UserToUserModel.FOLLOW, base_user=request.user, user=user)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

            if obj:
                obj.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)


class WatcherModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = UserWatchSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (FormParser, JSONParser)

    def get_queryset(self):
        return UserToUserModel.objects.filter(activity_type=UserToUserModel.WATCH, base_user=self.request.user)

    @action(detail=False)
    def save_count(self, request):
        total = UserToUserModel.objects.filter(activity_type=UserToUserModel.WATCH, base_user=request.user).count()
        return Response({'count': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        user_id = request.data.pop('user_id', None)
        username = request.data.pop('user_name', None)

        try:
            if user_id:
                user = User.objects.get(pk=user_id)
                obj = UserToUserModel.objects.get(activity_type=UserToUserModel.WATCH, base_user=request.user, user=user)
            elif username:
                user = User.objects.get(username=username)
                obj = UserToUserModel.objects.get(activity_type=UserToUserModel.WATCH, base_user=request.user, user=user)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

            if obj:
                obj.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist or MultipleObjectsReturned:
            return Response(status=status.HTTP_204_NO_CONTENT)
