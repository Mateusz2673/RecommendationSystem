from django.shortcuts import render
from django.shortcuts import redirect
from .models import Movies, Genredetails, Directorsdetails
from review_app.models import Reviews, Moviecomments
from django.views.decorators.http import require_POST
import requests
from django.conf import settings


# Create your views here.


def set_language(request):
    language = request.POST.get('language')
    if language in ['en', 'pl', 'de']:
        request.session['language'] = language
    # Przekierowanie na poprzednią stronę, aby odświeżyć widok
    return redirect(request.META.get('HTTP_REFERER', '/'))


def display_movie_details(request, movie_id):
    movie_details = Movies.get_movie_details(movie_id)
    reviews = Reviews.get_review_for_movie(movie_details['movie'])
    context = {
        'movie_details': movie_details,
        'reviews': reviews
    }
    return render(request, 'movie_details.html', context=context)


def display_movies(request):
    # Pobierz parametry z zapytania GET
    genre = request.GET.get('genre')
    production_year = request.GET.get('production_year')
    director = request.GET.get('director')

    sort_by = request.GET.get('sort_by', 'rating_desc')  # Domyślnie sortowanie po ratingu

    # Pobranie wszystkich dostępnych gatunków i reżyserów do listy rozwijanej
    genres = Genredetails.objects.all()
    directors = Directorsdetails.objects.all()

    # Obsługa różnych opcji sortowania
    if sort_by == 'rating_desc':
        filtered_movies = Movies.sort_movies(genre=genre, production_year=production_year, director=director,
                                             sort_by='-rating')
    elif sort_by == 'rating_asc':
        filtered_movies = Movies.sort_movies(genre=genre, production_year=production_year, director=director,
                                             sort_by='rating')
    elif sort_by == 'votes_desc':
        filtered_movies = Movies.sort_movies(genre=genre, production_year=production_year, director=director,
                                             sort_by='-votes')
    elif sort_by == 'votes_asc':
        filtered_movies = Movies.sort_movies(genre=genre, production_year=production_year, director=director,
                                             sort_by='votes')
    else:
        filtered_movies = Movies.sort_movies(genre=genre, production_year=production_year, director=director,
                                             sort_by=sort_by)

    # Ograniczenie liczby filmów do 100
    limited_movies = filtered_movies[:100]

    # Przekazanie przefiltrowanych filmów, dostępnych gatunków i reżyserów do szablonu
    return render(request, 'movies.html', {
        'movies_details': limited_movies,
        'genres': genres,
        'production_year': production_year,
        'directors': directors,
    })


def upcoming_movies(request):
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-EN&region=PL'

    response = requests.get(url)
    movies = response.json().get('results', [])

    base_image_url = "https://image.tmdb.org/t/p/w500"  # w500 to rozmiar obrazka
    for movie in movies:
        movie['poster_url'] = f"{base_image_url}{movie['poster_path']}"

    return render(request, 'upcoming_movies.html', {'movies': movies})
