from django.contrib import admin
from ArtworkLikeSaveApp.models import UserToArtworkModel


class UserToArtworkModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserToArtworkModel, UserToArtworkModelAdmin)