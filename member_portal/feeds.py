from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import addfeed_form
from datetime import datetime
from member_portal.models import feed_requests,feeds
import hashlib
from django.views import View   
from apps.models import android
import urllib.request, json
from hashids import Hashids

salt = 'This is my salt for test.'
hashids = Hashids(salt=salt,min_length=11)

# Dashboard
def dashboard(request):
    return render(request, 'dashboard.html')   

# For selecting app
def selectApp(request):
    return render(request,'selectApp.html')

# For adding feed to DB
def addfeed(request,appid_hash):

    appid = hashids.decode(appid_hash)
    if appid:
        appid = str(appid[0])
        store = 'AND'
        if request.method == 'POST':
            form = addfeed_form(request.POST)
            if form.is_valid():
                title = str(form.cleaned_data['title'])
                content = str(form.cleaned_data['content'])
                category = str(form.cleaned_data['category'])
                screenshots = str(form.cleaned_data['screenshots'])
                tags = str(form.cleaned_data['tags'])
                unique_str = title+'-'+content+'-'+store
                author = str(request.user)
                unique_hash = str(hashlib.sha256(unique_str.encode()).hexdigest())
                feed = feed_requests(
                    title=title,
                    appid=appid,
                    category=category,
                    store = store,
                    content = content,
                    author=author,
                    sshots = screenshots,
                    tags = tags,
                    unique_hash = unique_hash
                    )
                feed.save()
                print(unique_hash)
                return redirect('dashboard')
        else:
            form = addfeed_form()

        # Fetching From app data from appcubo.apps api
        details_url = "http://127.0.0.1:8000/apps/android/details/"+appid_hash
        with urllib.request.urlopen(details_url) as url:
            app = json.loads(url.read().decode())
        app = dict(app['results'][0])
        appName = app['title']
        appURL = app['app_url']
        publisher = app['publisher']
        publisherURL = app['publisher_url']
        price = app['price']
        icon = app['icon']
        # end of app data

    else:  # invalid app id selected (invalid url)
        return redirect('dashboard') 
    return render(request, 'addfeed.html',locals())

# For Ajax-Search
def searchApp(request):

    if request.method == 'POST':

        search_text = request.POST['search_text'].replace(' ','+')
        print (search_text)

        with urllib.request.urlopen("http://127.0.0.1:8000/apps/android/search/"+search_text) as url:
            search = json.loads(url.read().decode())

        context={
        'search':search["results"][:5],
        }

        return render(request,'ajax_search.html',context)

# For Pending Feed Requests ( ** For Staff Only ) 
def feedRequests(request):

    # Getting feed requests from from DB
    objs = feed_requests.objects.all()
    # Making Lists ready for data
    title = []
    appid = []
    category = []
    store = []
    content = []
    author = []
    created_at = []
    screenshots = []
    tags = []
    unique_hash = []
    app_data =[]

    if objs.exists():
        for feed in objs:
                title.append(feed.title)
                appid.append(feed.appid)
                if feed.category == "NR":
                    feed.category = '<button class="btn badge-soft-success btn-success btn-sm btn-round">NEW RELEASE</button>'
                elif feed.category == "DI":
                    feed.category = '<button class="btn badge-soft-warning btn-warning btn-sm btn-round">DISCOVER</button>'
                elif feed.category == "UP":
                    feed.category = '<button class="btn badge-soft-info btn-info btn-sm btn-round">UPDATED</button>'
                elif feed.category == "BF":
                    feed.category = '<button class="btn badge-soft-danger btn-danger btn-sm btn-round">BUGS & FIXES</button>'
                else:
                    feed.category = '<button class="btn badge-soft-dark btn-dark btn-sm btn-round">PRICE DROP</button>'
                category.append(feed.category)
                store.append(feed.store)
                content.append(feed.content)
                author.append(feed.author)
                created_at.append(feed.created_at)
                screenshots.append(feed.sshots)
                tags.append(feed.tags)
                unique_hash.append(feed.unique_hash)
                # Fetching From app data from appcubo.apps api
                details_url = "http://127.0.0.1:8000/apps/android/details/"+hashids.encode(feed.appid)
                with urllib.request.urlopen(details_url) as url:
                    app = json.loads(url.read().decode())
                app = dict(app['results'][0])
                app_data_temp = [app['title'],app['app_url'],app['publisher'],app['publisher_url'],app['price'],app['icon']]
                app_data.append(app_data_temp)
                # end of app data
    pendingFeed = zip(title,appid,category,store,content,author,created_at,screenshots,tags,unique_hash,app_data)

    return render(request,'feedRequests.html',locals())