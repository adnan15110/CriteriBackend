from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedIdentityField, ModelSerializer
from Art.models import Artwork, ArtCategory, ArtCollection
from UserAdministration.serialiazers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist


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
    categories = ArtCategoryNameOnlySerializer(many=True, read_only=False)

    class Meta:
        model = Artwork
        fields = ('url',
                  'image',
                  'title',
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

    class Meta:
        model = ArtCollection
        fields = ('url',
                  'title',
                  'collections',
                  'description',
                  'user',
                  )
        read_only_fields = (
            'created_at',
            'last_updated_at',)
