from django.db import models

# Create your models here.
class android(models.Model):
    title = models.CharField(max_length=255,default=None)
    publisher = models.CharField(max_length=300,default=None)
    app_url = models.CharField(max_length=255,default=None,unique=True)
    pub_url = models.CharField(max_length=255,default=None)
    cover = models.TextField(default=None)
    price = models.CharField(max_length=100,default=None)

class iOS(models.Model):
    title = models.CharField(max_length=255,default=None)
    publisher = models.CharField(max_length=255,default=None)
    app_url = models.CharField(max_length=255,default=None,unique=True)
    publisher_url = models.CharField(max_length=255,default=None)
    cover = models.TextField(default=None)
    price = models.CharField(max_length=100,default=None)
    appid = models.CharField(max_length=255,default=None,unique=True)
    devices = models.CharField(max_length=200,default=None)