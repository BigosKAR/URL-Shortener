from django.db import models

# Create your models here.
class UrlMapping(models.Model):
    id = models.BigIntegerField(primary_key=True)
    short_url = models.CharField(unique=True)
    original_url = models.CharField(null=False)