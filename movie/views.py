from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse("<h1>Welcome to the home page</h1>")
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name': 'Juan Andrés Young Hoyos'})
def about(request):
    return HttpResponse("<h1>Welcome to the about page</h1>")