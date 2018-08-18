from django.db import models
from django.contrib.auth.models import User
from Art.models import Artwork

# Create your models here.


class UserToArtworkModel(models.Model):
    '''
    Saves user's like and save relationship
    '''
    LIKE = 'Like'
    SAVE = 'Save'
    ACTION_TYPES = (
        (LIKE, LIKE),
        (SAVE, SAVE),
    )

    user = models.ForeignKey(User, related_name='related_arts', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    artwork = models.ForeignKey(Artwork, related_name='related_user', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'UserToArtworkActions'

    def __str__(self):
        return '{} {} {}'.format(self.user.username, self.activity_type, self.artwork.title)
