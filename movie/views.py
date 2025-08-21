from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
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

def statistics_view(request):
    matplotlib.use('Agg')  # Establecer el backend de Matplotlib en 'Agg'
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    
    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}
    
    # Filtrar las películas por año y género y contar la cantidad
    for movie in all_movies:
        # Contar por año
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
        
        # Contar por género (considerar solo el primer género)
        if movie.genre:
            # Dividir por comas y tomar el primer género
            first_genre = movie.genre.split(',')[0].strip()
            if first_genre in movie_counts_by_genre:
                movie_counts_by_genre[first_genre] += 1
            else:
                movie_counts_by_genre[first_genre] = 1
        else:
            # Películas sin género
            if "Sin género" in movie_counts_by_genre:
                movie_counts_by_genre["Sin género"] += 1
            else:
                movie_counts_by_genre["Sin género"] = 1
    
    # Crear figura con dos subplots (dos gráficas lado a lado)
    # Opciones de tamaño:
    # figsize=(12, 5)  - Más compacto
    # figsize=(15, 6)  - Tamaño actual (bueno para pantallas grandes)
    # figsize=(18, 8)  - Más grande y detallado
    # figsize=(20, 10) - Muy grande para presentaciones
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 3))
    
    # GRÁFICA 1: Películas por año
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    ax1.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')
    ax1.set_title('Movies per year', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of movies')
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(movie_counts_by_year.keys(), rotation=90)
    ax1.grid(True, alpha=0.3)
    
    # GRÁFICA 2: Películas por género
    bar_positions_genre = range(len(movie_counts_by_genre))
    
    ax2.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center', color='lightcoral')
    ax2.set_title('Movies per genre', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Genre')
    ax2.set_ylabel('Number of movies')
    ax2.set_xticks(bar_positions_genre)
    ax2.set_xticklabels(movie_counts_by_genre.keys(), rotation=45, ha='right')
    ax2.grid(True, alpha=0.3)
    
    # Ajustar el espaciado
    plt.tight_layout()
    
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})
