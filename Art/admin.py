from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Art.models import Artwork, ArtCollection, ArtCategory


class ArtworkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artwork, ArtworkAdmin)


class ArtCollectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(ArtCollection, ArtCollectionAdmin)


class ArtCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(ArtCategory, ArtCategoryAdmin)
