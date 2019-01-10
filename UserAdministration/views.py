from rest_framework.viewsets import ModelViewSet
from UserAdministration.serialiazers import UserProfileSerializer, UserSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import authentication, viewsets, mixins
from UserAdministration.models import Profile, Address
from django.contrib.auth.models import User
# Create your views here.


class ProfileViewSet(ModelViewSet):
    """
    retrieve:
        Return the given profile.

    list:
        Return a list of profiles (only the logged in user).

    create:
        Create a empty profile instance with an user and empty address.

    update:
        Updates profile information

    partial_update:
        Partially updates profile information.
        Update information about address and user using their corresponding api (available under the 'url' key).

    delete:
        Deletes an profile.
        """
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class UserViewSet(ModelViewSet):
    """
        retrieve:
            Return the given user.

        list:
            Return a list of users.

        create:
            Create a user with empty profile through signal.

        update:
            Updates user information.

        partial_update:
            Partially updates user information

        delete:
            Deletes an user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    parser_classes = (JSONParser, FormParser)


class AddressViewSet(ModelViewSet):
    """
    retrieve:
        Return the given address.
    list:
        Return a list of all the existing address.

    create:
        Create a new address instance.

    update:
        Updates an address

    partial_update:
        Partially update an address

    delete:
        Deletes an address.
        """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication)
    parser_classes = (JSONParser, FormParser)