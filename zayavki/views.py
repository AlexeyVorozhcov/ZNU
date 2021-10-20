from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "zayavki/index.html")

def zayavki(request):
    return render(request, "zayavki/zayavki.html")    