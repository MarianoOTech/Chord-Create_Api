from django.conf import settings
from django.db import models

# Create your models here.
class Link(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Link', related_name='votes', on_delete=models.CASCADE)