from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import *


def HomeView(request):
    return render(request, 'app/home.html')


