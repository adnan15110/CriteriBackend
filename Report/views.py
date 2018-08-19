from rest_framework.viewsets import ModelViewSet
from Report.serializers import ArtworkReportSerializer
from Report.models import ArtworkReport
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


class ArtworkReportViewSet(ModelViewSet):
    queryset = ArtworkReport.objects.all()
    serializer_class = ArtworkReportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    parser_classes = (JSONParser, FormParser, MultiPartParser )

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)