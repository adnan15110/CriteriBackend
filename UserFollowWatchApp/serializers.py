from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, ValidationError, HyperlinkedIdentityField
from django.contrib.auth.models import User
from UserFollowWatchApp.models import UserToUserModel
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class UserRelationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class UserFollowSerializer(ModelSerializer):
    base_user = UserRelationSerializer(many=False, read_only=True)
    user = UserRelationSerializer(many=False, read_only=True)

    class Meta:
        model = UserToUserModel
        fields = ('user', 'base_user')
        read_only_fields = (
            'activity_type',)

    def create(self, validated_data):
        user = self.context['request'].user
        username_to_follow = self.initial_data.pop('username', None)  # non-model field so not present in validated data

        try:
            user_to_follow = User.objects.get(username=username_to_follow)
            if user:
                obj = UserToUserModel(base_user=user, activity_type=UserToUserModel.FOLLOW, user=user_to_follow)
                obj.save()
        except ObjectDoesNotExist:
            raise ValidationError('User not found', code=status.HTTP_204_NO_CONTENT)
        except MultipleObjectsReturned:
            raise ValidationError('Multiple Object returned', code=status.HTTP_204_NO_CONTENT)

        return obj


class UserWatchSerializer(ModelSerializer):
    base_user = UserRelationSerializer(many=False, read_only=True)
    user = UserRelationSerializer(many=False, read_only=True)

    class Meta:
        model = UserToUserModel
        fields = ('user', 'base_user')
        read_only_fields = (
            'activity_type',)

    def create(self, validated_data):

        user = self.context['request'].user
        username_to_watch = self.initial_data.pop('username', None)  # non-model field so not present in validated data

        try:
            user_to_watch = User.objects.get(username=username_to_watch)
            if user:
                obj = UserToUserModel(base_user=user, activity_type=UserToUserModel.WATCH, user=user_to_watch)
                obj.save()
        except ObjectDoesNotExist:
            raise ValidationError('User not found', code=status.HTTP_204_NO_CONTENT)
        except MultipleObjectsReturned:
            raise ValidationError('Multiple Object returned', code=status.HTTP_204_NO_CONTENT)
        return obj

