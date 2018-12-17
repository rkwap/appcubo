from django.db import models

# Create your models here.
class android(models.Model):
    title = models.CharField(max_length=255,default=None)
    publisher = models.CharField(max_length=300,default=None)
    app_url = models.TextField(default=None)
    pub_url = models.CharField(max_length=300,default=None)
    cover = models.TextField(default=None)
    price = models.CharField(max_length=100,default=None)