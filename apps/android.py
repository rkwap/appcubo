from django.http import HttpResponse
import datetime
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from apps.models import android
from member_portal.templatetags.encryption import encode,decode
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission,IsAuthenticated,IsAdminUser
from apps.serializers import androidSerializer

# Searching the play store,storing in db & fetching from db
# input : /android/search/<search_text>

class search(APIView):
    # permission_classes = (IsAuthenticated,)
    # Cache requested url for each user for 10 hours
    @method_decorator(cache_page(60*60*10))
    @method_decorator(vary_on_cookie)
    def get(self, request,q):
        # Scraping the app details
        q = q.replace(' ','+')
        page = requests.get('https://play.google.com/store/search?q='+q+'&c=apps')
        soup = BeautifulSoup(page.text, 'html.parser')

        raw_title = soup.find_all('a',class_='title')
        raw_pub = soup.find_all('a',class_='subtitle')
        raw_cover = soup.find_all('img',class_='cover-image')
        raw_price = soup.find_all('span',class_='display-price')

        for info in zip(raw_title,raw_pub,raw_cover,raw_price):
            # Temporary parameters
            t_title = str(info[0].attrs['title'])
            t_app_url =str('https://play.google.com'+info[0].attrs['href'])
            t_pub = str(info[1].text)
            t_pub_url = str('https://play.google.com'+info[1].attrs['href'])
            t_cover = str(info[2].attrs['src'])
            t_id = 0
            if str(info[3].text) != '':
                t_price = str(info[3].text)
            else:
                t_price = 'Free'
            ######
            objs = android.objects.filter(app_url=t_app_url)
            if not objs.exists():
                app = android(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover,price=t_price)
                app.save()

        q = q.replace('+',' ')

        apps = android.objects.filter(title__icontains=q)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = androidSerializer(apps, many=True)
        return Response({"results": serializer.data})



# input1 : /android/details/<app_id> eg. com.roposo.android
#   Provides full app details (all parameters like developer address,download count etc.)
# input 2 : /android/details/<id_hashed> eg. Ko2nR2rnEb9
#   Provides neccessary app details from db

class details(APIView):
    @method_decorator(cache_page(60*60*10))
    @method_decorator(vary_on_cookie)
    def get(self, request,playid):
        playid_hash = playid
        playid_decoded = str(decode(playid_hash))
        apps = android.objects.filter(id=playid_decoded)   

        # if app already exists, then fetch details from DB
        if apps.exists() and playid_decoded !='0':
            # the many param informs the serializer that it will be serializing more than a single article.
            serializer = androidSerializer(apps, many=True)
            data = {"results": serializer.data}
        # else scrap the data and save it in DB. 
        # Also provides full details when only google appid is provided.
        else:
            # Scraping the app details
            page = requests.get('https://play.google.com/store/apps/details?id='+playid)
            soup = BeautifulSoup(page.text, 'html.parser')
            title = soup.find('h1',class_='AHFaub').text  #title
            appid = playid #appid
            pub_cat = soup.find_all('a',class_='hrTbp R8zArc')
            publisher = pub_cat[0].text #publisher
            publisher_url = soup.find('a',class_='hrTbp R8zArc').attrs['href'] #publisher_url
            icon = soup.find('img',class_='T75of ujDFqe').attrs['src'] #icon
            category = pub_cat[1].text #category
            reviews = soup.find('span',class_='AYi5wd TBRnV').text #reviews
            # sshots = soup.find_all('img',class_='T75of lxGQyd')
            # screenshots = []
            # for s in sshots:
            #     screenshots.append(s.attrs['src']) #screenshots
            video = str(soup.find('div',class_='TdqJUe'))
            pos1 = video.find('https://www.youtube.com/')
            pos2 = video.find('" jsaction="')
            video = video[pos1:pos2] #video
            des = soup.find('content')
            description=des.text #description
            description_html = str(des).replace('<content><div jsname="sngebd">','').replace('</content>','').replace('</div>','')
            #description_html
            ec = soup.find('span',class_='giozf')
            if ec is not None:
                editors_choice = 'True' #editors_choice
            else:
                editors_choice = 'False'
            developer_id = str(publisher_url).replace('https://play.google.com/store/apps/dev?id=','') #developer_id
            additional = soup.find_all('span',class_='htlgb')
            updated = additional[1].text #updated
            size = additional[2].text #size
            installs = additional[4].text #installs
            current_version = additional[6].text #current_version
            required_android_version = additional[8].text #required_android_version
            dev = soup.find_all('a',class_='hrTbp ')
            developer_url = dev[1].attrs['href'] #developer_url
            developer_email = soup.find('a',class_='hrTbp KyaTEc').text #developer_email
            developer_address = additional[-1].text
            pos1 = str(developer_address).find('Privacy Policy')
            developer_address = developer_address[pos1:].replace('Privacy Policy','') #developer_address
            url = 'https://play.google.com/store/apps/details?id='+playid #url
            price = soup.find_all('button')
            price = price[-1].text.replace('$0.00','') #price
            if price == '':
                price = 'Free'    

            objs = android.objects.filter(title=title,publisher=publisher,app_url=url,pub_url=publisher_url,cover=icon,price=price)  
            if not objs.exists():
                app = android(title=title,publisher=publisher,app_url=url,pub_url=publisher_url,cover=icon,price=price)
                app.save()
            
            id = encode(objs[0].id)

            keys = ['id','title','appid','publisher','publisherURL','icon','category','reviews','video','description','description_html','editors_choice','developer_id','updated','size','installs','current_version','required_android_version','developer_url','developer_email','developer_address','appURL','price']
            values = [id,title,appid,publisher,publisher_url,icon,category,reviews,video,description,description_html,editors_choice,developer_id,updated,size,installs,current_version,required_android_version,developer_url,developer_email,developer_address,url,price]
            appdata = [dict(zip(keys,values))]

            data = {"results": appdata}

        return Response(data)











#####---------------------------------------------------------------##################
## For function based drf views ###
# from rest_framework.decorators import api_view
# from rest_framework.decorators import parser_classes


# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS
########### function based view or ########
# @api_view(['get'])
# def all(request):
#     apps = android.objects.all()[:15]
#     # the many param informs the serializer that it will be serializing more than a single article.
#     serializer = androidSerializer(apps, many=True)
#     return Response({"results": serializer.data})
######## class based view ##############

## --------------------------------------------------------------------------######
## --------------------------------------------------------------------------######
