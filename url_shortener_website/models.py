from django.db import models

# Create your models here.
class UrlMapping(models.Model):
    shortcode = models.PositiveIntegerField(primary_key=True, unique=True)
    original_url = models.CharField(null=False)