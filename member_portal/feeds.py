from django.shortcuts import render,redirect
from django.http import HttpResponse
from member_portal.models import feed_requests,feeds # Importing member_portal models
from member_portal.forms import addfeed_form # Importing Forms
from apps.models import android # Importing appstore models
from member_portal.decorators import ajax_required # Ajax-requests-only decorator
from member_portal.templatetags.encryption import encode,decode,encode_alpha,decode_alpha # For youtube-like encrpytion
from member_portal.templatetags.essentials import store_ltos,store_stol
from datetime import datetime # Datetime Library
import hashlib # Importing hashlib for hashing functions
from django.views import View
import urllib.request, json # For handaling json files
from django.db.models import Q # Django Q objects for query
from django.contrib.auth.decorators import login_required # login_required decorator
from apps.main import app_details,search_app # Importing app_details and search_app function
from django.core.paginator import Paginator
from django.urls import reverse



# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html',locals())   

# For Selecting app
@login_required
def selectApp(request,store):
    if store=='stores':
        return render(request,'selectStore.html')
    elif store=='android' or store=='ios':
        return render(request,'selectApp.html',locals())
    else:
        return redirect('/dashboard')

# For Ajax-Search
@login_required
def searchApp(request):

    if request.method == 'POST':

        search_text = request.POST['search_text'].replace(' ','+')
        store = request.POST.get('store',False)
        print (search_text)
        print(store)
        search = search_app(request,search_text,store)
        search = search[:5]
        return render(request,'ajax_search.html',locals())
    else:
        return redirect("/dashboard")

# For Adding/Posting feed (request) to DB (table : feed_requests)
@login_required
def addfeed(request,store,appid_hash):

    appid = decode(appid_hash)
    if appid:
        store = store_ltos(store)
        if store=='':
            return redirect('/dashboard')
        else:
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
                    if request.user.is_staff :
                        feed = feeds(
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
                    else:    
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
                    return redirect('dashboard')
            else:
                form = addfeed_form()

            store=store_stol(store)
            # Fetching From app data from appcubo.apps api
            # For APP details along form
            app = app_details(request,appid_hash,store) # app_details function

            appName = app['title']
            appURL = app['appURL']
            publisher = app['publisher']
            publisherURL = app['publisherURL']
            price = app['price']
            icon = app['icon']
            # end of app data
    else:  # invalid app id selected (invalid url)
        return redirect('dashboard') 
    return render(request, 'feedAddEdit.html',locals())

# For Pending Feed Requests ( ** For Staff Only ) 
@login_required
def feedRequests(request):
    if request.user.is_staff :
        # For sorting of feeds
        store = request.GET.get('store', False)
        if store:
            store = store_ltos(store)
            # Getting feed requests from from DB
            objs = feed_requests.objects.filter(store__icontains=store).order_by('-id')
        else:
            objs = feed_requests.objects.all().order_by('-id')

        RequestCount = objs.count()

        paginator = Paginator(objs, 3)
        page = request.GET.get('page')
        feedsCount = paginator.get_page(page)

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
        feed_id=[]

        if objs.exists():
            for feed in objs:
                    title.append(feed.title)
                    appid.append(encode(feed.appid))
                    if feed.category == "NR":
                        feed.category = '<button class="btn badge-success btn-success btn-sm btn-round">NEW RELEASE</button>'
                    elif feed.category == "DI":
                        feed.category = '<button class="btn badge-warning btn-warning btn-sm btn-round">DISCOVER</button>'
                    elif feed.category == "UP":
                        feed.category = '<button class="btn badge-info btn-info btn-sm btn-round">UPDATED</button>'
                    elif feed.category == "BF":
                        feed.category = '<button class="btn badge-danger btn-danger btn-sm btn-round">BUGS & FIXES</button>'
                    else:
                        feed.category = '<button class="btn badge-dark btn-dark btn-sm btn-round">PRICE DROP</button>'
                    category.append(feed.category)
                    store.append(feed.store)
                    content.append(feed.content)
                    author.append(feed.author)
                    created_at.append(feed.created_at)
                    screenshots.append(feed.sshots)
                    tags.append(feed.tags)
                    unique_hash.append(feed.unique_hash)
                    feed_id.append(encode_alpha(feed.id))
                    print(feed_id)
                    feed.store = store_stol(feed.store)
                    # Getting app data
                    app = app_details(request,encode(feed.appid),feed.store) # app_details function
                    app_data_temp = [app['title'],app['appURL'],app['publisher'],app['publisherURL'],app['price'],app['icon']]
                    app_data.append(app_data_temp)
                    # end of app data
        pendingFeed = list(zip(title,appid,category,store,content,author,created_at,screenshots,tags,unique_hash,app_data,feed_id))

        return render(request,'feedRequests.html',locals())
    else:
        return redirect('dashboard')

# For Reviewing the pending feed request ( ** For Staff Only)
@login_required
def pendingReview(request):
    if request.user.is_staff :
        if request.method == 'POST':
            # if post request made from feedRequests
            if 'review' in request.POST:
                unique_hash = str(request.POST.get('key', False))
                appid_hash = str(request.POST.get('appid', False))

                # Fetching requested feed data from DB
                obj = feed_requests.objects.filter(unique_hash=unique_hash)
                title = obj[0].title
                category = obj[0].category
                content = obj[0].content
                author = obj[0].author
                sshots = obj[0].sshots
                tags = obj[0].tags
                store = obj[0].store
                created_at = obj[0].created_at
                # end of feed data
                store = store_stol(store)
                # Fetching From app data from appcubo.apps api
                app = app_details(request,appid_hash,store)
                appName = app['title']
                appURL = app['appURL']
                publisher = app['publisher']
                publisherURL = app['publisherURL']
                price = app['price']
                icon = app['icon']
                # end of app data
                pending = True
                form = addfeed_form(initial={'title': title, 'category' : category, 'content' : content, 'screenshots' : sshots, 'tags' : tags})

            # if post request made by submitting the feed
            # (Accept Feed)
            elif 'acceptFeed' in request.POST:

                form = addfeed_form(request.POST)
                if form.is_valid():
                    title = str(form.cleaned_data['title'])
                    content = str(form.cleaned_data['content'])
                    category = str(form.cleaned_data['category'])
                    screenshots = str(form.cleaned_data['screenshots'])
                    tags = str(form.cleaned_data['tags'])
                    author = str(request.POST.get('author', False))
                    unique_hash = str(request.POST.get('key', False)) 
                    store = str(request.POST.get('store', False))
                    appid_hash = str(request.POST.get('appid_hash', False))
                    appid = decode(appid_hash)

                    # Saving the object in feeds tables
                    feed = feeds(
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

                    # Delete Object from feed_requests table
                    feed_requests.objects.filter(unique_hash=unique_hash).delete()

                    return redirect('feedRequests')
            elif 'rejectFeed' in request.POST:
                unique_hash = str(request.POST.get('key', False))
                # Delete Object from feed_requests table
                feed_requests.objects.filter(unique_hash=unique_hash).delete()
                return redirect('feedRequests')
                
            else:
                return redirect('feedRequests')
                

            return render(request,'feedAddEdit.html',locals())
    else:
        return redirect('dashboard')

    return render(request,'feedAddEdit.html',locals())

# For user feeds
@login_required
def userFeeds(request):
    
    # For sorting of feeds
    store = request.GET.get('store', False)
    if store:
        store = store_ltos(store)
        # Getting feed requests from from DB
        objs = feeds.objects.filter(Q(store__icontains=store) & Q(author=str(request.user))).order_by('-id')
    else:
        objs = feeds.objects.filter(author=str(request.user)).order_by('-id')

    feedCount = objs.count()

    paginator = Paginator(objs, 3)
    page = request.GET.get('page')
    feedsCount = paginator.get_page(page)


    # print(paginator)
    # Making Lists ready for data
    title = []
    appid = []
    category = []
    store = []
    content = []
    author = []
    created_at = []
    updated_at = []
    screenshots = []
    tags = []
    unique_hash = []
    app_data =[]
    feed_id=[]
    upvote_count = []
    downvote_count = []
    comment_count = []

    if objs.exists():
        for feed in objs:
                title.append(feed.title)
                appid.append(encode(feed.appid))
                if feed.category == "NR":
                    feed.category = '<button class="btn badge-success btn-success btn-sm btn-round">NEW RELEASE</button>'
                elif feed.category == "DI":
                    feed.category = '<button class="btn badge-warning btn-warning btn-sm btn-round">DISCOVER</button>'
                elif feed.category == "UP":
                    feed.category = '<button class="btn badge-info btn-info btn-sm btn-round">UPDATED</button>'
                elif feed.category == "BF":
                    feed.category = '<button class="btn badge-danger btn-danger btn-sm btn-round">BUGS & FIXES</button>'
                else:
                    feed.category = '<button class="btn badge-dark btn-dark btn-sm btn-round">PRICE DROP</button>'
                category.append(feed.category)
                store.append(feed.store)
                content.append(feed.content)
                author.append(feed.author)
                created_at.append(feed.created_at)
                screenshots.append(feed.sshots)
                tags.append(feed.tags)
                unique_hash.append(feed.unique_hash)
                feed_id.append(encode_alpha(feed.id))
                feed.store = store_stol(feed.store)
                if feed.upvote_count is None:
                    feed.upvote_count='0'
                if feed.downvote_count is None:
                    feed.downvote_count = '0'
                if feed.comment_count is None:
                    feed.comment_count = '0'
                
                upvote_count.append(feed.upvote_count)
                downvote_count.append(feed.downvote_count)
                comment_count.append(feed.comment_count)
                # Getting app data
                app = app_details(request,encode(feed.appid),feed.store) # app_details function

                app_data_temp = [app['title'],app['appURL'],app['publisher'],app['publisherURL'],app['price'],app['icon']]
                app_data.append(app_data_temp)
                # end of app data
    myFeed = list(zip(title,appid,category,store,content,author,created_at,screenshots,tags,unique_hash,app_data,feed_id,upvote_count,downvote_count,comment_count))

    return render(request,'userFeeds.html',locals())

@login_required
def editFeed(request):
    if request.method == 'POST':
        # if post request made from feedRequests
        if 'editFeed' in request.POST:
            appid_hash = str(request.POST.get('appid', False))
            feed_id_hashed = str(request.POST.get('feed_id', False))
            feed_id = decode_alpha(feed_id_hashed)
            # Fetching requested feed data from DB
            obj = feeds.objects.filter(id=feed_id)
            title = obj[0].title
            category = obj[0].category
            content = obj[0].content
            author = obj[0].author
            sshots = obj[0].sshots
            tags = obj[0].tags
            store = obj[0].store
            created_at = obj[0].created_at
            updated_at = obj[0].updated_at
            # end of feed data
            store = store_stol(store)
            # Fetching From app data from appcubo.apps api
            app = app_details(request,appid_hash,store)
            appName = app['title']
            appURL = app['appURL']
            publisher = app['publisher']
            publisherURL = app['publisherURL']
            price = app['price']
            icon = app['icon']
            # end of app data
            edit = True
            form = addfeed_form(initial={'title': title, 'category' : category, 'content' : content, 'screenshots' : sshots, 'tags' : tags})

        # if post request made by submitting the feed
        # (Accept Feed)
        elif 'acceptFeed' in request.POST:
            form = addfeed_form(request.POST)
            if form.is_valid():
                title = str(form.cleaned_data['title'])
                content = str(form.cleaned_data['content'])
                category = str(form.cleaned_data['category'])
                screenshots = str(form.cleaned_data['screenshots'])
                tags = str(form.cleaned_data['tags'])
                feed_id = decode_alpha(str(request.POST.get('feed_id', False)))
                # Updating the object in feeds tables
                feed = feeds.objects.get(id=feed_id)
                feed.title=title
                feed.content=content
                feed.category=category
                feed.sshots=screenshots
                feed.tags=tags
                feed.save()   

                return redirect('userFeeds')
        elif 'rejectFeed' in request.POST:
            feed_id = decode_alpha(str(request.POST.get('feed_id', False)))
            # Delete Object from feed_requests table
            feeds.objects.filter(id=feed_id).delete()
            return redirect('userFeeds')
            
        else:
            return redirect('userFeeds')
            

        return render(request,'feedAddEdit.html',locals())

    return render(request,'feedAddEdit.html',locals())

