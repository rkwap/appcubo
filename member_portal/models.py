from django.db import models
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

CATEGORY_CHOICES = (
    ("NR", "New Release"),
    ("DI", "Discovery"),
    ("UP", "Update"),
    ("BF", "Bugs and Fixes"),
    ("PD", "Price Drop"),
)
STORE_CHOICES = (
    ("AND", "Android"),
    ("IOS", "iOS"),
    ("UWP", "UWP"),
    ("PWA", "Progressive Web App"),
    ("LIN", "Linux"),
    ("W32", "Win32"),
    ("MAC", "Mac OS"),
)
class feeds(models.Model):
    title = models.CharField(max_length=255,default=None)
    appid = models.BigIntegerField(default=None)
    category = models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=None)
    store = models.CharField(max_length=3,choices=STORE_CHOICES,default=None)
    # content = models.TextField(default=None)
    content = RichTextUploadingField()
    author = models.CharField(max_length=150,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    sshots = models.ImageField(upload_to=user_directory_path,null=True,default=None)
    upvote_count = models.IntegerField(blank=True, null=True,default=None)
    downvote_count = models.IntegerField(blank=True, null=True,default=None)
    comment_count = models.IntegerField(blank=True, null=True,default=None)
    upvoters = models.TextField(null=True,default=None)
    downvoters = models.TextField(null=True,default=None)
    tags = models.TextField(default=None)
    dev_response = models.TextField(null=True,default=None)
    unique_hash = models.CharField(max_length=255,unique=True,default=None)

class feed_requests(models.Model):
    title = models.CharField(max_length=255,default=None)
    appid = models.BigIntegerField(default=None)
    category = models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=None)
    store = models.CharField(max_length=3,choices=STORE_CHOICES,default=None)
    # content = models.TextField(default=None)
    content = RichTextUploadingField()
    author = models.CharField(max_length=150,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    sshots = models.ImageField(upload_to=user_directory_path,null=True,default=None)
    tags = models.TextField(default=None)
    unique_hash = models.CharField(max_length=255,unique=True,default=None)