from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

#from . import models
#from . import forms


def home(request):
    context = {
            "title":"Greetings",
            "opener":"Hello World",
            "initialStatement":" This is the beginnings of the best ball fantasy site",
            }
    return render(request, "home.html", context=context)
