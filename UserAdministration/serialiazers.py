from rest_framework.serializers import HyperlinkedModelSerializer
from django.contrib.auth.models import User
from UserAdministration.models import Profile, Address


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email')


class AddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url',
                  'apt_number',
                  'street_number',
                  'street_name',
                  'neighbourhood',
                  'city',
                  'province',
                  'postal_code',
                  'country',
                  )


class UserProfileSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=False)
    address = AddressSerializer(many=False, read_only=False)

    class Meta:
        model = Profile
        fields = ('url',
                  'user',
                  'address',
                  'small_profile_image',
                  'large_profile_image',
                  'headline',
                  'biography',
                  'website',
                  'date_of_birth',
                  'profile_level',
                  'small_profile_image',
                  'created_at',
                  'last_updated_at',
                  )

    def update(self, instance, validated_data):
        user_dict = validated_data.pop('user', None)
        if user_dict:
            user_obj = instance.user
            for key, value in user_dict.items():
                setattr(user_obj, key, value)
            user_obj.save()
            validated_data["user"] = user_obj

        address_dict = validated_data.pop('address', None)
        if address_dict:
            address_obj = instance.address
            for key, value in address_dict.items():
                setattr(address_obj, key, value)
            address_obj.save()
            validated_data["address"] = address_obj

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
