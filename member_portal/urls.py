from django.urls import path, include
from member_portal import mp_main

urlpatterns = [
    path('', include('allauth.urls')),
    path('dashboard/', mp_main.dashboard , name='dashboard'),
    path('addfeed/', mp_main.addfeed , name='addfeed'),
]
