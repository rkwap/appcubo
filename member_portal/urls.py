from django.urls import path, include
from member_portal import feeds

urlpatterns = [
    path('accounts/', include('allauth.urls')), # for accounts
    path('dashboard/', feeds.dashboard , name='dashboard'), # dashboard
    path('addfeed/<str:appid_hash>/post/', feeds.addfeed , name='addfeed'), # posting feed in addfeed
    path('addfeed/selectapp/', feeds.selectApp , name='selectapp'), # selecting app
    path('addfeed/search', feeds.searchApp , name='searchApp'), #render ajax_search.html
    path('feedrequests/', feeds.feedRequests , name='feedRequests')

]
