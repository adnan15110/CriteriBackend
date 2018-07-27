from django.db import models
from django.contrib.auth.models import User
import uuid


def unique_image_path(instance, filename):
    file_type = filename.split('.')[1]
    return '{}_{}/{}.{}'.format(instance.user.username, instance.user.id, uuid.uuid4(), file_type)


class Address(models.Model):
    """
        Users address model
    """
    apt_number = models.IntegerField(blank=True, null=True)
    street_number = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(blank=True, null=True, max_length=50)
    neighbourhood = models.CharField(blank=True, null=True, max_length=30)
    city = models.CharField(blank=True, null=True, max_length=30)
    province = models.CharField(blank=True, null=True, max_length=30)
    postal_code = models.CharField(blank=True, null=True, max_length=15)
    country = models.CharField(blank=True, null=True, max_length=30)

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return "Apt {},{} {}, {}, {}, {}".format(self.apt_number,
                                                 self.street_number,
                                                 self.street_name,
                                                 self.city,
                                                 self.province,
                                                 self.postal_code,
                                                 self.country
                                                 )


PROFILE_CHOICES = (
    ('ProfilePlus', 'ProfilePlus'),
    ('ProfileLite', 'ProfileLite'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='address')
    # images
    large_profile_image = models.FileField(upload_to=unique_image_path, blank=True)
    small_profile_image = models.FileField(upload_to=unique_image_path, blank=True)
    # info
    headline = models.CharField(max_length=200, null=True, blank=True)
    biography = models.TextField(blank=True, null=True, max_length=500)
    website = models.CharField(blank=True, null=True, max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_level = models.CharField(max_length=20, null=True, choices=PROFILE_CHOICES, default=PROFILE_CHOICES[0][1])
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Profile'

    def __str__(self):
        return "{}-{}".format(self.user.username, self.user.id)
