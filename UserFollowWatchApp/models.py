from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserToUserModel(models.Model):
    '''
    Saves user's like and save relationship
    '''
    FOLLOW = 'Follow'
    WATCH = 'Watch'
    ACTION_TYPES = (
        (FOLLOW, FOLLOW),
        (WATCH, WATCH),
    )

    base_user = models.ForeignKey(User, related_name='related', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTION_TYPES)
    user = models.ForeignKey(User, related_name='related_by', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'UserToUserActions'

    def __str__(self):
        return '{} {} {}'.format(self.base_user.username, self.activity_type, self.user.username)
