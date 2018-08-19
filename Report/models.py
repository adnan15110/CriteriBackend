from django.db import models
from Art.models import Artwork
from django.contrib.auth.models import User


# Create your models here.
class ArtworkReport(models.Model):
    """
    Captures user's report about artwork
    """
    INAPPROPRIATE_CONTENT = 'Inappropriate Content'
    STOLEN_PROPERTY = 'Stolen Property'
    ACTION_TYPES = (
        (INAPPROPRIATE_CONTENT, INAPPROPRIATE_CONTENT),
        (STOLEN_PROPERTY, STOLEN_PROPERTY),
    )
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'
    REVIEWED = 'Reviewed'
    STATUS_TYPE = (
        (PENDING, PENDING),
        (CANCELLED, CANCELLED),
        (REVIEWED, REVIEWED)
    )

    artwork = models.ForeignKey(Artwork, related_name='reports', on_delete=models.CASCADE)
    report_type = models.CharField(max_length=30, choices=ACTION_TYPES, default=STOLEN_PROPERTY)
    report_status = models.CharField(max_length=30, choices=STATUS_TYPE, default=PENDING)
    reporter = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    description = models.TextField(max_length=100, default='')
    reported_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        db_table = 'Reports'

    def __str__(self):
        return 'Report: {} - {}'.format(self.artwork.title, self.report_type)
