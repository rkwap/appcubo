from django.urls import path, include
from apps import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api, name='api'),
    path('android/search/<str:q>/', views.play, name='playAppSearch'),
    path('android/details/<str:playid>/', views.playAppDetails, name='playAppDetails')

]
