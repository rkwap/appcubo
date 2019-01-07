import urllib.request, json # For handaling json files
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
import requests


def search_app(q,store):
    if store== "android":
        search_url = reverse('playAppSearch', args=[q])
    elif store == "ios":
        search_url = reverse('iOSApps', args=[q])
    else:
        search_url = ""
    if search_url!="":
        search_url = "http://127.0.0.1:8000"+search_url

        search = requests.get(search_url, verify=False).json()
        # with urllib.request.urlopen(search_url) as url:
        #     search = json.loads(url.read().decode())
        return search['results'] # returns list
    else:
        return redirect('/dashboard')

def app_details(appid,store):
    if store== "android":
        details_url = reverse('playAppDetails', args=[appid])
    elif store == "ios":
        details_url = reverse('iOSApps', args=[appid])
    elif store == "uwp":
        details_url = reverse('UWPAppDetails', args=[appid])
    else:
        details_url = ""
    
    if details_url!="":

        details_url = "http://127.0.0.1:8000"+details_url
        app = requests.get(details_url, verify=False).json()

        # with urllib.request.urlopen(details_url) as url:
        #     app = json.loads(url.read().decode())
        return dict(app['results'][0]) # returns dictionary
    else:
        return redirect('/dashboard')