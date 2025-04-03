from django.http import HttpResponse
from django.shortcuts import render
def home(request):
    #return HttpResponse("Hello Bhai")
    return render(request,"index.html")

def contact(request):
    return HttpResponse("Hello Bhai contact")

def about(request):
    return HttpResponse("about us")

