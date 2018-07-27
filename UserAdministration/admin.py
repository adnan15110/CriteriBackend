from django.contrib import admin
from UserAdministration.models import Profile, Address


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Profile, UserProfileAdmin)


# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Address, AddressAdmin)
