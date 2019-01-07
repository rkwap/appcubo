from django.urls import path, include
from apps import android,ios
from apps.android import search,details # for class based view
from apps.ios import apps
from apps.uwp import searchUWP,detailsUWP

urlpatterns = [
    path('android/search/<str:q>/', search.as_view(),name='playAppSearch'), # for class based views
    path('android/details/<str:playid>/', details.as_view(),name='playAppDetails'),
    path('ios/<str:q>/', apps.as_view(), name='iOSApps'),
    path('uwp/search/<str:q>/', searchUWP.as_view(),name='UWPAppSearch'),
    path('uwp/details/<str:uwpid>/', detailsUWP.as_view(),name='UWPAppDetails'),

]
