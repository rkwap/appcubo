from django.http import HttpResponse
import datetime
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from apps.models import iOS
from apps.main import app_details
from member_portal.templatetags.encryption import encode,decode # For youtube-like encrpytion
import urllib.request, json # For handaling json files
from django.db.models import Q # Django Q objects for query

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission,IsAuthenticated,IsAdminUser
from apps.serializers import iOSSerializer


# input1: /apps/ios/<search_text> eg. search_text = instagram
#   -> Copy results from Apple API, stores data in DB and returns DB results
# input 2: /apps/ios/<appid> eg. appid = 389801252
#   -> Retrives result from Apple API, stores data in DB and returns DB results.
# input 3: /apps/ios/<encoded_id> eg. encoded_id = 4X28nAYn53G
#   -> Provies results from DB.
class apps(APIView):
    @method_decorator(cache_page(60*60*10))
    @method_decorator(vary_on_cookie)
    def get(self,request,q):
        # for a single app details
        id_hash = q
        id_decoded = decode(id_hash)
        apps = iOS.objects.filter(id=id_decoded)   
        
        # if app already exists, then fetch details from DB
        if apps.exists() and id_decoded !='0':
            serializer = iOSSerializer(apps, many=True)
            data = {"results": serializer.data}
        else:
            # For searching apps 
            # Scraping the app details
            q = q.replace(' ','+')
            with urllib.request.urlopen('https://itunes.apple.com/search?term='+q+'&entity=iPadSoftware,software&limit=30') as url:
                search = json.loads(url.read().decode())
                search = search['results'] # returns list

            # Getting app parameters
            for app in search:
                t_appid = str(app['trackId'])

                apps = iOS.objects.filter(appid=t_appid)
                if not apps.exists():
                    # Checking for devices supported 
                    for device in app['supportedDevices']:
                        if 'iPhone' in device:
                            iPhone = True
                            break
                        else:
                            iPhone = False
                    for device in app['supportedDevices']:
                        if 'iPad' in device:
                            iPad = True
                            break
                        else:
                            iPad = False
                    if iPhone is False :
                        device = "iPad Only"
                    if iPad is False :
                        device = "iPhone Only" 
                    if iPhone is True and iPad is True :
                        device = "Both iPhone and iPad"       
                    # end of checking devices 

                    t_title = str(app['trackName'])
                    t_publisher = str(app['artistName'])
                    t_app_url = str(app['trackViewUrl'])
                    t_publisher_url = str(app['artistViewUrl'])
                    t_cover = str(app['artworkUrl512'].replace('512x512','200x200'))
                    t_price = app.get('formattedPrice','')

                    t_devices = str(device)
                    # End of getting app parameters

                    # Saving the app details to DB
                    obj = iOS(title=t_title,publisher=t_publisher,app_url=t_app_url,publisher_url=t_publisher_url,cover=t_cover,price=t_price,appid=t_appid,devices=t_devices)
                    obj.save()
                    

            # Searching from DB
            q = q.replace('+',' ')
            apps = iOS.objects.filter(Q(title__icontains=q) | Q(appid__icontains=q) | Q(publisher__icontains=q))[:5]
            # the many param informs the serializer that it will be serializing more than a single article.
            serializer = iOSSerializer(apps, many=True)
            data = {"results": serializer.data}

        return Response(data)







