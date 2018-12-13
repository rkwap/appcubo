from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'dashboard.html')


def addfeed(request):


    return render(request, 'addfeed.html',locals())