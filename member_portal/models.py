from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class feeds(models.Model):
    NEWRELEASE = 'NR'
    DISCOVERY = 'DI'
    UPDATE = 'UP'
    BUGSFIXES = 'BF'
    PRICEDROP = 'PD'
    CATEGORY_CHOICES = (
        (NEWRELEASE, "New Release"),
        (DISCOVERY, "Discovery"),
        (UPDATE, "Update"),
        (BUGSFIXES, "Bugs and Fixes"),
        (PRICEDROP, "Price Drop"),
    )
    ANDROID = 'AND'
    IOS = 'IOS'
    UWP = 'UWP'
    PWA = 'PWA'
    LINUX = 'LIN'
    WIN32 = 'W32'
    MACOS = 'MAC'
    STORE_CHOICES = (
        (ANDROID, "Android"),
        (IOS, "iOS"),
        (UWP, "UWP"),
        (PWA, "Progressive Web App"),
        (LINUX, "Linux"),
        (WIN32, "Win32"),
        (MACOS, "Mac OS"),
    )
    title = models.CharField(max_length=255,default=None,unique=True)
    appid = models.BigIntegerField(default=None)
    category = models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=None)
    store = models.CharField(max_length=3,choices=STORE_CHOICES,default=None)
    content = models.TextField(default=None)
    author = models.IntegerField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sshots = models.ImageField(upload_to=user_directory_path,default=None)
    upvote_count = models.IntegerField(default=None)
    downvote = models.IntegerField(default=None)
    comment_count = models.IntegerField(default=None)
    upvoters = models.TextField(default=None)
    downvoters = models.TextField(default=None)
    tags = models.TextField(default=None)
    dev_response = models.TextField(default=None)