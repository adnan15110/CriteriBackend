from django.contrib import admin
from UserFollowWatchApp.models import UserToUserModel


class UserToUserModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserToUserModel, UserToUserModelAdmin)
