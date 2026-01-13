from django.shortcuts import render
from django.http import JsonResponse
from . models import Booking
from .models import models
from .models import Attendee


# Create your views here.
def index(request):
    return render(request,'BBMS/index2.html')

def base(request):
    return render(request,'base.html')


