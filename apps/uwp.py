from django.http import HttpResponse
import datetime
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from apps.models import android,UWP
from member_portal.templatetags.encryption import encode,decode
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission,IsAuthenticated,IsAdminUser
from apps.serializers import androidSerializer,UWPSerializer
from apps.main import app_details

# Searching the play store,storing in db & fetching from db
# input : /android/search/<search_text>

class searchUWP(APIView):
    # permission_classes = (IsAuthenticated,)
    # Cache requested url for each user for 10 hours
    # @method_decorator(cache_page(60*60*10))
    # @method_decorator(vary_on_cookie)
    def get(self, request,q):
        # Scraping the app details
        q = q.replace(' ','+')
        page = requests.get('https://www.microsoft.com/en-us/store/search/apps?q='+q)
        soup = BeautifulSoup(page.text, 'html.parser')

        # appid=[]
        raw_ids = soup.find_all('div',class_='m-channel-placement-item')
        data=[]
        for app in raw_ids[:1]:
            appid= app.attrs['data-id']
            app = app_details(appid,'uwp')
            print(app)
        return Response({"results": data})



# input1 : /android/details/<app_id> eg. com.roposo.android
#   Provides full app details (all parameters like developer address,download count etc.)
# input 2 : /android/details/<id_hashed> eg. Ko2nR2rnEb9
#   Provides neccessary app details from db

class detailsUWP(APIView):
    # @method_decorator(cache_page(60*60*10))
    # @method_decorator(vary_on_cookie)
    def get(self, request,uwpid):
        uwpid_hash = uwpid
        uwpid_decoded = str(decode(uwpid_hash))
        apps = UWP.objects.filter(id=uwpid_decoded)   

        # if app already exists, then fetch details from DB
        if apps.exists() and uwpid_decoded !='0':
            # the many param informs the serializer that it will be serializing more than a single article.
            serializer = UWPSerializer(apps, many=True)
            data = {"results": serializer.data}
        # else scrap the data and save it in DB. 
        # Also provides full details when only google appid is provided.
        else:
            # Scraping the app details
            url= 'https://www.microsoft.com/en-us/p/app/'+uwpid
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            appid = uwpid #appid
            title = soup.find('h1', {'id':'DynamicHeading_productTitle'}).text #title
            publisher = soup.find('span', {'role':'text'}).text #publisher
            icon = soup.find('meta', {'property':'og:image'}).attrs['content']
            icon = icon.replace('//','http://').replace('w=120&h=120&q=60','w=200&h=200') #icon
            catinfo = soup.find('a', {'class':'c-hyperlink'}) 
            category = catinfo.text #category
            category_url = 'https://www.microsoft.com'+str(catinfo.attrs['href']) #category_url
            rating = soup.find_all('span', {'role':'presentation'})
            ratingCount= rating[-1].text #ratingCount
            ratingValue= rating[-2].text #ratingValue
            sshots = soup.find_all('img', {'class':'lazyload f-screenshot-fixed-size'})
            screenshots = [] #screenshots
            for shot in sshots:
                sshot = shot.attrs['data-src'].replace('//','http://').replace('?w=672&h=378&q=80&mode=letterbox&background=%23FFE4E4E4&format=jpg','')
                screenshots.append(sshot)
            description = soup.find('p', {'class':'c-paragraph pi-product-description-text'}).text #description
            price = soup.find('meta', {'itemprop':'price'}).attrs['content'] #price
            publisherURL='' 


            objs = UWP.objects.filter(title=title,publisher=publisher,app_url=url,cover=icon,price=price,appid=appid)  
            if not objs.exists():
                app = UWP(title=title,publisher=publisher,app_url=url,cover=icon,price=price,appid=appid)
                app.save()
            
            id = encode(objs[0].id)

            keys = ['id','title','appid','publisher','publisherURL','icon','category','category_url','ratingCount','ratingValue','description','appURL','price','screenshots']
            values = [id,title,appid,publisher,publisherURL,icon,category,category_url,ratingCount,ratingValue,description,url,price,screenshots]
            appdata = [dict(zip(keys,values))]

            data = {"results": appdata}

        return Response(data)




