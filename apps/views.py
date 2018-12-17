from django.http import HttpResponse
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from .forms import SearchApp
from apps.models import android
from hashids import Hashids

salt = 'This is my salt for test.'
hashids = Hashids(salt=salt,min_length=11)

def play(request,q):
    # Scraping the app details
    q = q.replace(' ','+')
    page = requests.get('https://play.google.com/store/search?q='+q+'&c=apps')
    soup = BeautifulSoup(page.text, 'html.parser')

    raw_title = soup.find_all('a',class_='title')
    raw_pub = soup.find_all('a',class_='subtitle')
    raw_cover = soup.find_all('img',class_='cover-image')
    raw_price = soup.find_all('span',class_='display-price')

    ids = []
    title = []
    pub = []
    app_url = []
    pub_url = []
    cover = []
    price=[]
    
    for info in zip(raw_title,raw_pub,raw_cover,raw_price):

        # Temporary parameters
        t_title = str(info[0].attrs['title']).encode('latin-1', 'ignore').decode('latin-1')
        t_app_url =str('https://play.google.com'+info[0].attrs['href'])
        t_pub = str(info[1].text).encode('latin-1', 'ignore').decode('latin-1')
        t_pub_url = str('https://play.google.com'+info[1].attrs['href'])
        t_cover = str(info[2].attrs['src'])
        t_id = 0
        if str(info[3].text) != '':
            t_price = str(info[3].text)
        else:
            t_price = 'Free'
        ######

        objs = android.objects.filter(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover,price=t_price)
       
        if objs.exists():
            t_id = objs[0].id
            t_title = objs[0].title
            t_app_url = objs[0].app_url
            t_pub = objs[0].publisher
            t_pub_url = objs[0].pub_url
            t_price = objs[0].price
            t_cover = objs[0].cover
        else:
            app = android(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover,price=t_price)
            app.save()
            t_id = app.id
            t_title = app.title
            t_app_url = app.app_url
            t_pub = app.publisher
            t_pub_url = app.pub_url
            t_price = app.price
            t_cover = app.cover


        ids.append(t_id)
        title.append(t_title)
        app_url.append(t_app_url)
        pub.append(t_pub)
        pub_url.append(t_pub_url)
        cover.append(t_cover)
        price.append(t_price)

    if request.method == 'POST':
        form = SearchApp(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = SearchApp()

    keys = ['id','title','appURL','publisher','publisherURL','icon','price']
    values = list(zip(ids,title,app_url,pub,pub_url,cover,price))

    app_details = []

    for value in values:
        app_details.append(dict(zip(keys,value)))

    data = {"results": app_details}
    return JsonResponse(data)




def playAppDetails(request,playid):
    playid_hash = playid
    playid_decoded = hashids.decode(playid_hash)
    if playid_decoded :
        playid_decoded = str(playid_decoded[0])
    else :
        playid_decoded = 0
    objs = android.objects.filter(id=playid_decoded)   

    # if app already exists, then fetch details from DB
    if objs.exists():
        title = objs[0].title
        app_url = objs[0].app_url
        publisher = objs[0].publisher
        publisher_url = objs[0].pub_url
        price = objs[0].price
        icon = objs[0].cover
        keys = ['title','app_url','publisher','publisher_url','price','icon']
        values = [title,app_url,publisher,publisher_url,price,icon]
        appdata = [dict(zip(keys,values))]
        data = {"results": appdata}
        return JsonResponse(data)

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
        
        id = hashids.encode(objs[0].id)

        keys = ['id','title','appid','publisher','publisher_url','icon','category','reviews','video','description','description_html','editors_choice','developer_id','updated','size','installs','current_version','required_android_version','developer_url','developer_email','developer_address','url','price']
        values = [id,title,appid,publisher,publisher_url,icon,category,reviews,video,description,description_html,editors_choice,developer_id,updated,size,installs,current_version,required_android_version,developer_url,developer_email,developer_address,url,price]


        appdata = [dict(zip(keys,values))]
        data = {"results": appdata}

        return JsonResponse(data)



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
    price=[]
    
    for info in zip(raw_title,raw_pub,raw_cover,raw_price):

        # Temporary parameters
        t_title = str(info[0].attrs['title']).encode('latin-1', 'ignore').decode('latin-1')
        t_app_url =str('https://play.google.com'+info[0].attrs['href'])
        t_pub = str(info[1].text).encode('latin-1', 'ignore').decode('latin-1')
        t_pub_url = str('https://play.google.com'+info[1].attrs['href'])
        t_cover = str(info[2].attrs['src'])
        if str(info[3].text) != '':
            t_price = str(info[3].text)
        else:
            t_price = 'Free'
        ######

        objs = android.objects.filter(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover,price=t_price)
       
        if objs.exists():
            t_title = objs[0].title
            t_app_url = objs[0].app_url
            t_pub = objs[0].publisher
            t_pub_url = objs[0].pub_url
            t_price = objs[0].price
            t_cover = objs[0].cover
        else:
            app = android(title=t_title,publisher=t_pub,app_url=t_app_url,pub_url=t_pub_url,cover=t_cover,price=t_price)
            app.save()  

        title.append(t_title)
        app_url.append(t_app_url)
        pub.append(t_pub)
        pub_url.append(t_pub_url)
        cover.append(t_cover)
        price.append(t_price)  

    if request.method == 'POST':
        form = SearchApp(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = SearchApp()

    return render(request, 'index.html', {'test': zip(title,app_url,pub,pub_url,cover,price) , 'form' : form, 'q' : q })


def api(request):
    MAX_OBJECTS = 20
    apps_objs = android.objects.all()[:MAX_OBJECTS]
    data = {"results": list(apps_objs.values("id", "title", "publisher"))}
    return JsonResponse(data)