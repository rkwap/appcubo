from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

