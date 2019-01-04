from django import template
register = template.Library()
from member_portal.models import feed_requests,feeds # Importing member_portal models
from django.shortcuts import render


@register.filter(name='fr_count')
def fr_count(variable):
    return feed_requests.objects.all().count()

@register.filter(name='myf_count')
def myf_count(username):
    return feeds.objects.filter(author=username).count()