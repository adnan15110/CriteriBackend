"""CriteriBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from UserAdministration.urls import user_admin_router
from UserFollowWatchApp.urls import user_preference_router
from ArtworkLikeSaveApp.urls import artwork_preference_router
from Report.urls import report_router
from Art.urls import art_router
from FrontendApi.urls import urlpatterns as frontend_api_url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(user_admin_router.urls)),
    path('api/v1/', include(art_router.urls)),
    path('api/v1/', include(user_preference_router.urls)),
    path('api/v1/', include(artwork_preference_router.urls)),
    path('api/v1/', include(report_router.urls)),
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += frontend_api_url

if settings.DEBUG and settings.MODULE == 'Test':
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
