from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedIdentityField, ModelSerializer, \
    SerializerMethodField
from Art.models import Artwork, ArtCategory, ArtCollection
from UserAdministration.serialiazers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from ArtworkLikeSaveApp.models import UserToArtworkModel


class ArtCategorySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="art-category-detail")

    class Meta:
        model = ArtCategory
        fields = ('url', 'category_name', 'details')
        read_only_fields = ('created_at',)


class ArtCategoryNameOnlySerializer(ModelSerializer):
    class Meta:
        model = ArtCategory
        fields = ('category_name',)


class ArtworkTitleOnlySerializer(ModelSerializer):
    class Meta:
        model = Artwork
        fields = ('id', 'title',)


class ArtworkSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    categories = SerializerMethodField(read_only=False)
    like = SerializerMethodField(read_only=True)
    saved = SerializerMethodField(read_only=True)

    class Meta:
        model = Artwork
        fields = ('url',
                  'id',
                  'image',
                  'title',
                  'like',
                  'saved',
                  'categories',
                  'width',
                  'height',
                  'unit',
                  'description',
                  'user',
                  )
        read_only_fields = (
            'created_at',
            'last_updated_at',)

    def get_categories(self, obj):
        data = []
        for category in obj.categories.all():
            data.append(category.category_name)
        return data

    def get_like(self, obj):
        like_count = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.LIKE, artwork=obj).count()

        if like_count > 0:
            return {'liked': True, 'like_count': like_count}
        else:
            return {'liked': False, 'like_count': like_count}

    def get_saved(self, obj):
        save_count = UserToArtworkModel.objects.filter(activity_type=UserToArtworkModel.SAVE, artwork=obj).count()
        return True if save_count > 0 else False

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        obj = Artwork.objects.create(**validated_data)
        obj.save()

        for category in categories:
            try:
                category_obj = ArtCategory.objects.get(category_name=category["category_name"])
                obj.categories.add(category_obj)
            except ObjectDoesNotExist:
                pass
        return obj

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', [])
        user = validated_data.pop('user', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        for category in categories:
            try:
                category_obj = ArtCategory.objects.get(category_name=category["category_name"])
                instance.categories.add(category_obj)
            except ObjectDoesNotExist:
                pass
        instance.save()
        return instance


class ArtCollectionSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="art-collection-detail")
    user = UserSerializer(many=False, read_only=True)
    collections = ArtworkTitleOnlySerializer(many=True, read_only=True)
    artworks = ArtworkSerializer(many=True, read_only=True)

    class Meta:
        model = ArtCollection
        fields = ('url',
                  'title',
                  'collections',
                  'description',
                  'user',
                  'artworks'
                  )
        read_only_fields = (
            'created_at',
            'last_updated_at',)


class ArtCollectionViewOnlySerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="art-collection-detail")

    class Meta:
        model = ArtCollection
        fields = ('url',
                  'title',
                  'description',
                  )
        read_only_fields = (
            'created_at',
            'last_updated_at',)