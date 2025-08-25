from django.shortcuts import render
from .models import Movie
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64
# Create your views here.

def home(request):
    #return HttpResponse("<h1>Welcome to the home page</h1>")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Juan Andrés Young Hoyos ;)'})

    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies, 'name': 'Juan Andrés Young Hoyos'})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):

    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Contar películas por año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Ancho y posiciones de barras
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    # Gráfica de barras (UNA sola)
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    
    plt.subplots_adjust(bottom=0.3)

    # Guardar a base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    year_graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    genre_counts = {}
    for movie in all_movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
        else:
            first_genre = "Sin género"
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    bar_positions_genre = range(len(genre_counts))
    
    plt.figure() 
    plt.bar(bar_positions_genre, genre_counts.values(), width=bar_width, align='center')
    plt.title('Movies per genre (first genre)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, genre_counts.keys(), rotation=45)
    plt.subplots_adjust(bottom=0.3)

    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    genre_graphic = base64.b64encode(buffer_genre.getvalue()).decode('utf-8')
    buffer_genre.close()
    plt.close()

    #Renderizar la plantilla pero esta vez para las dos gráficas
    return render(request, 'statistics.html', {'graphic': year_graphic, 'genre_graphic': genre_graphic})