from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
def unique_image_path(instance, filename):
    file_type = filename.split('.')[1]
    return '{}_{}/{}.{}'.format(instance.user.username, instance.user.id, uuid.uuid4(), file_type)


class ArtCategory(models.Model):
    """
    Artwork models
    """
    category_name = models.CharField(max_length=50, default='')
    details = models.CharField(max_length=200, default='')
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'ArtCategory'

    def __str__(self):
        return '{}'.format(self.category_name)


class Artwork(models.Model):
    """
    Artwork models
    """
    user = models.ForeignKey(User, related_name='artworks', on_delete=models.CASCADE)
    image = models.FileField(upload_to=unique_image_path, blank=True, null=True)
    title = models.CharField(max_length=200, default='')
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    unit = models.CharField(max_length=20, default='inch')
    categories = models.ManyToManyField(ArtCategory, related_name='artworks')
    description = models.TextField(max_length=300)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'Art'

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.title)


class ArtCollection(models.Model):
    """
    Art Collection model
    """
    user = models.ForeignKey(User, related_name='art_collections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(max_length=300, default='')
    artworks = models.ManyToManyField(Artwork, related_name='artworks')
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'ArtCollection'

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.title)