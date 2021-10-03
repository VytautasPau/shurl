from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Url(models.Model):
    url = models.TextField(name="url")  # real url
    active = models.BooleanField(default=True, name="active")

    created_at = models.DateTimeField(auto_now_add=True, name="created")
    updated_at = models.DateTimeField(auto_now=True, name="updated")

    clicks = models.IntegerField(default=0, name="clicks")
    max_clicks = models.IntegerField(default=0, name="max_clicks")  # 0 = no limit

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, name="user")


class UrlIndex(models.Model):
    url = models.TextField(name="url")  # encrypted string (shurl)
    data = models.ForeignKey(Url, on_delete=models.CASCADE, name="url_data")

    class Meta:
        indexes = [models.Index(fields=['url', ])]


