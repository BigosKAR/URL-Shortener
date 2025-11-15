from django.db import models

# Create your models here.

class UrlMapping(models.Model):
    id = models.BigAutoField(primary_key=True) # Support massive amounts of entry IDs (for example: 100 million new URLs every day)
    shortcode = models.CharField(unique=True)
    original_url = models.CharField(null=False, unique=True)
    clicks = models.BigIntegerField(default=0)

class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, null=False)
    hashed_password = models.CharField(null=False)

class UserUrlMapping(models.Model):
    user_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    url_id = models.ForeignKey(UrlMapping, on_delete=models.CASCADE)
