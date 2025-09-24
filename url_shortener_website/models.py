from django.db import models

# Create your models here.
class UrlMapping(models.Model):
    id = models.BigAutoField(primary_key=True) # Support massive amounts of entry IDs (for example: 100 million new URLs every day)
    shortcode = models.CharField(unique=True)
    original_url = models.CharField(null=False)