from django.http import HttpResponse
import datetime
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .forms import SearchApp
from apps.models import Android


def index(request):
    # Scraping the app details
    q = request.GET.get("q", "")
    page = requests.get('https://play.google.com/store/search?q='+q+'&c=apps')
    soup = BeautifulSoup(page.text, 'html.parser')

    raw_title = soup.find_all('a',class_='title')
    raw_pub = soup.find_all('a',class_='subtitle')
    raw_cover = soup.find_all('img',class_='cover-image')
    raw_price = soup.find_all('span',class_='display-price')

    title = []
    pub = []
    app_url = []
    pub_url = []
    cover = []
    cover_lg =[]
    price=[]
    
    for info in zip(raw_title,raw_pub,raw_cover,raw_price):

        # Temporary parameters
        t_title = str(info[0].attrs['title']).encode('latin-1', 'ignore').decode('latin-1')
        t_app_url =str('https://play.google.com'+info[0].attrs['href'])
        t_pub = str(info[1].text).encode('latin-1', 'ignore').decode('latin-1')
        t_pub_url = str('https://play.google.com'+info[1].attrs['href'])
        t_cover = str(info[2].attrs['src'])
        t_cover_lg = str(info[2].attrs['data-cover-large'])
        t_cover_all = str(t_cover+','+t_cover_lg)
        if str(info[3].text) != '':
            t_price = str(info[3].text)
        else:
            t_price = 'Free'
        ######

        objs = Android.objects.filter(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover_all,price=t_price)
       
        if objs.exists():
            t_title = objs[0].title
            t_app_url = objs[0].app_url
            t_pub = objs[0].publisher
            t_pub_url = objs[0].pub_url
            t_price = objs[0].price
            covers = str(objs[0].cover).split(',')
            t_cover = covers[0]
            t_cover_lg = covers[1]
        else:
            app = Android(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover_all,price=t_price)
            app.save()  

        title.append(t_title)
        app_url.append(t_app_url)
        pub.append(t_pub)
        pub_url.append(t_pub_url)
        cover.append(t_cover)
        cover_lg.append(t_cover_lg)
        price.append(t_price)  

    if request.method == 'POST':
        form = SearchApp(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = SearchApp()

    return render(request, 'index.html', {'test': zip(title,app_url,pub,pub_url,cover,cover_lg,price) , 'form' : form, 'q' : q })
