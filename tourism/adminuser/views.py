
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import *


def DashboardView(request):
    return render(request, 'adminuser/dashboard.html')
