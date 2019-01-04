from django.contrib import admin
from .models import feed_requests,feeds
# Register your models here.
admin.site.register(feeds)
admin.site.register(feed_requests)