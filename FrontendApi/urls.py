from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from FrontendApi.views import MainFeedView, UserDetailApiView, ProfileDetailApiView

urlpatterns = [
    url(r'api/v1/main-feed-info/$', MainFeedView.as_view()),
    url(r'api/v1/user-info/$', UserDetailApiView.as_view()),
    url(r'api/v1/profile-info/$', ProfileDetailApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)