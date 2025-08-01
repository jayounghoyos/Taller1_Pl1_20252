from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
# Create your views here.

def home(request):
    #return HttpResponse("<h1>Welcome to the home page</h1>")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Juan Andrés Young Hoyos ;)'})

    seachTerm = request.GET.get('searchMovie')
    if seachTerm:
        movies = Movie.objects.filter(title__icontains=seachTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': seachTerm, 'movies': movies, 'name': 'Juan Andrés Young Hoyos'})

def about(request):
    return render(request, 'about.html', {'name': 'Juan Andrés Young Hoyos '})
