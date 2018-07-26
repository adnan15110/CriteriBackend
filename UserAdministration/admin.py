from django.contrib import admin
from UserAdministration.models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')


admin.site.register(UserProfile, UserProfileAdmin)
