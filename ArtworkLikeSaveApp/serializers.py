from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, ValidationError, \
    HyperlinkedIdentityField, SerializerMethodField
from django.contrib.auth.models import User
from ArtworkLikeSaveApp.models import UserToArtworkModel
from Art.models import Artwork
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from UserAdministration.models import Profile
from UserAdministration.serialiazers import UserProfileSerializer



class UserRelationSerializer(HyperlinkedModelSerializer):
    image = SerializerMethodField(read_only=False)
    class Meta:
        model = User
        fields = ('url', 'username', 'image')

    def get_image(self, obj):
        data = UserProfileSerializer(obj.profile, context={'request': self.context['request']}).data
        return data['small_profile_image']


class ArtworkRelationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Artwork
        fields = ('url', 'title')


class ArtworkLikeSerializer(ModelSerializer):
    user = UserRelationSerializer(many=False, read_only=True)
    artwork = ArtworkRelationSerializer(many=False, read_only=True)

    class Meta:
        model = UserToArtworkModel
        fields = ('user', 'artwork')
        read_only_fields = (
            'activity_type',)

    def create(self, validated_data):
        user = self.context['request'].user
        artwork_id_to_like = self.initial_data.pop('artwork_id', None)  # non-model field so not present in validated data
        artwork_title_to_like = self.initial_data.pop('artwork_title', None)

        try:
            artwork_to_like = Artwork.objects.get(pk=artwork_id_to_like, title=artwork_title_to_like)
            if user:
                obj_counts = UserToArtworkModel.objects.filter(user=user,
                                                               activity_type=UserToArtworkModel.LIKE,
                                                               artwork=artwork_to_like).count()
                if obj_counts == 0:
                    obj = UserToArtworkModel(user=user, activity_type=UserToArtworkModel.LIKE, artwork=artwork_to_like)
                    obj.save()
        except ObjectDoesNotExist:
            raise ValidationError('Artwork not found', code=status.HTTP_204_NO_CONTENT)
        except MultipleObjectsReturned:
            raise ValidationError('Multiple Artwork Object returned', code=status.HTTP_204_NO_CONTENT)

        return obj


class ArtworkSaveSerializer(ModelSerializer):
    user = UserRelationSerializer(many=False, read_only=True)
    artwork = ArtworkRelationSerializer(many=False, read_only=True)

    class Meta:
        model = UserToArtworkModel
        fields = ('user', 'artwork')
        read_only_fields = (
            'activity_type',)

    def create(self, validated_data):
        user = self.context['request'].user
        artwork_id_to_save = self.initial_data.pop('artwork_id', None)  # non-model field so not present in validated data
        artwork_title_to_save = self.initial_data.pop('artwork_title', None)

        try:
            artwork_to_save =Artwork.objects.get(pk=artwork_id_to_save, title=artwork_title_to_save)
            if user:
                obj = UserToArtworkModel(user=user, activity_type=UserToArtworkModel.SAVE, artwork=artwork_to_save)
                obj.save()
        except ObjectDoesNotExist:
            raise ValidationError('Artwork not found', code=status.HTTP_204_NO_CONTENT)
        except MultipleObjectsReturned:
            raise ValidationError('Multiple Artwork Object returned', code=status.HTTP_204_NO_CONTENT)

        return obj