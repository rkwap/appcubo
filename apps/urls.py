from django.urls import path, include
from apps import android,ios
from apps.android import search,details # for class based view
from apps.ios import apps

urlpatterns = [
    path('android/search/<str:q>/', search.as_view(),name='playAppSearch'), # for class based views
    path('android/details/<str:playid>/', details.as_view(),name='playAppDetails'), # for class based views
    path('ios/<str:q>/', apps.as_view(), name='iOSApps'), # for class based views


]
