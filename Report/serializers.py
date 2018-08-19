from rest_framework.serializers import ModelSerializer, ValidationError, HyperlinkedRelatedField
from Report.models import ArtworkReport
from ArtworkLikeSaveApp.serializers import UserRelationSerializer
from Art.serializers import ArtworkSerializer
from Art.models import Artwork
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class ArtworkReportSerializer(ModelSerializer):
    artwork = HyperlinkedRelatedField(many=False, read_only=False, queryset=Artwork.objects.all(), view_name='artwork-detail')
    reporter = UserRelationSerializer(many=False, read_only=True)

    class Meta:
        model = ArtworkReport
        fields = ('id',
                  'artwork',
                  'reporter',
                  'report_status',
                  'report_type',
                  'description',
                  )
        read_only_fields = (
            'reported_at',
            'last_updated',
        )
