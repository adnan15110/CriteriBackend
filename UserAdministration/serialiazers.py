from rest_framework.serializers import HyperlinkedModelSerializer
from django.contrib.auth.models import User
from UserAdministration.models import UserProfile


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email')


class UserProfileSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=False)

    class Meta:
        model = UserProfile
        fields = ('url', 'user', 'bio', 'location', 'birth_date')

    def update(self, instance, validated_data):
        user_dict = validated_data.pop('user', None)
        if user_dict:
            user_obj = instance.user
            for key, value in user_dict.items():
                setattr(user_obj, key, value)
            user_obj.save()
            validated_data["user"] = user_obj
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

