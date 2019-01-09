from rest_framework.viewsets import GenericViewSet
from  rest_framework import status
from rest_framework import mixins
from UserFollowWatchApp.serializers import UserFollowSerializer, UserWatchSerializer
from UserFollowWatchApp.models import UserToUserModel
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Create your views here.


class FollowerModelViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
        list:
            Return a list of Followers for the logged in user.

        create:
            Create a follower relation from logged in user to the user in the request.
            params: {'username': string}
    """
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (JSONParser, FormParser)

    def get_queryset(self):
        return UserToUserModel.objects.filter(activity_type=UserToUserModel.FOLLOW)

    @action(detail=False)
    def follow_count(self, request):
        """
        Returns the number of followers of the logged in user.
        :param request: None
        :return:
        """
        total = UserToUserModel.objects.filter(activity_type=UserToUserModel.FOLLOW, base_user=request.user).count()
        return Response({'follower': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        """
        removes the follow request
        :param request: {'user_id':number, 'user_name':string}
        :return:
        """
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
    """
        list:
            Return a list of Watchers for the logged in user.

        create:
            Create a watcher relation from logged in user to the user in the request.
            params: {'username': string}
    """
    serializer_class = UserWatchSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication,SessionAuthentication)
    parser_classes = (JSONParser, FormParser)

    def get_queryset(self):
        return UserToUserModel.objects.filter(activity_type=UserToUserModel.WATCH)

    @action(detail=False)
    def watch_count(self, request):
        """
        returns watch count
        :param request:
        :return:
        """
        total = UserToUserModel.objects.filter(activity_type=UserToUserModel.WATCH, base_user=request.user).count()
        return Response({'count': total})

    @action(methods=['post'], detail=False)
    def remove(self, request):
        """
        removes a watcher relation from logged in user to the user in the request.
        params: {'username': string}
         :return:
        """
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
