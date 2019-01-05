from django.urls import path, include
from member_portal import feeds

urlpatterns = [
    path('accounts/', include('allauth.urls')), # for accounts
    path('dashboard/', feeds.dashboard , name='dashboard'), # dashboard
    path('addfeed/<str:store>/<str:appid_hash>/post/', feeds.addfeed , name='addfeed'), # posting feed in addfeed
    path('addfeed/selectapp/<str:store>/', feeds.selectApp , name='selectApp'), # selecting app
    path('addfeed/search', feeds.searchApp , name='searchApp'), #render ajax_search.html
    path('feedrequests/', feeds.feedRequests , name='feedRequests'),
    path('feedrequests/review/', feeds.pendingReview , name='pendingReview'),
    path('myfeeds/edit/', feeds.editFeed , name='editFeed'),
    path('myfeeds/', feeds.userFeeds , name='userFeeds')


]
