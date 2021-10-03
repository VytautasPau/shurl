from django.contrib import admin

# Register your models here.
from app_shurl.models import Url


class UrlAdmin(admin.ModelAdmin):
    pass


admin.site.register(Url, UrlAdmin)
