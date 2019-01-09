from rest_framework.viewsets import ModelViewSet
from Report.serializers import ArtworkReportSerializer
from Report.models import ArtworkReport
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class ArtworkReportViewSet(ModelViewSet):
    """
    retrieve:
        Return the given report of artwork.

    list:
        Return a list of artwork reports.

    create:
        Create an artwork report.
        sample request body:

        {
        "artwork": "http://localhost:8000/api/v1/artwork/1/",
        "report_status": "Pending",
        "report_type": "Stolen Property",
        "description": "Testing the api"
        }


    update:
        Updates an artwork report.

    partial_update:
        Partially updates an artwork report.

    delete:
        Deletes an artwork report.
        """
    queryset = ArtworkReport.objects.all()
    serializer_class = ArtworkReportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
