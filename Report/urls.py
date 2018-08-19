from rest_framework.routers import DefaultRouter
from Report.views import ArtworkReportViewSet

report_router=DefaultRouter()
report_router.register('artwork-report', ArtworkReportViewSet, base_name='artwork-report')