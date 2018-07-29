from rest_framework.viewsets import ModelViewSet
from UserAdministration.serialiazers import UserProfileSerializer, UserSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import authentication
from UserAdministration.models import Profile, Address
from django.contrib.auth.models import User
# Create your views here.


class ProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.BasicAuthentication)
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.BasicAuthentication)
    parser_classes = (JSONParser, FormParser)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.BasicAuthentication)
    parser_classes = (JSONParser, FormParser)