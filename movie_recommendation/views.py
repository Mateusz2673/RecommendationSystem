from django.shortcuts import render
from movie_app.models import Movies
from review_app.models import Reviews
from movie_recommendation.models import MovieRecommender
from user_app.models import Users

def homepage(request):
    popular_movies = Movies.get_popular_movies()
    print(type(popular_movies[0]))
    print(popular_movies)
    use_content = 'use_content' in request.POST
    use_collaborative = 'use_collaborative' in request.POST
    print(f"use_collaborative: {use_collaborative}")
    print(f"use_content: {use_content}")
    recommended_movies = MovieRecommender(count=6).movie_recommendations(
       movie=Movies.get_movies(), use_content=use_content, use_collaborative=use_collaborative
    )
    latest_reviews = Reviews.get_latest_review()
    context = {
        'popular_movies': popular_movies,
        'latest_reviews': latest_reviews,
        'recommended_movies': recommended_movies,
        'range': range(1, 6)
    }
    return render(request, 'index.html', context=context)

def about(request):
    return render(request, 'about.html')


def search_view(request):
    query = request.GET.get('q', '').strip()
    movies = Movies.objects.filter(title__icontains=query).distinct('title') if query else []
    return render(request, 'search_results.html', {'movies': movies})

def search_movies(request):
    query = request.GET.get('q', '').strip()
    if query:
        movies = Movies.objects.filter(title__icontains=query)[:8]
        results = [{'id': movie.movie_id, 'title': movie.title} for movie in movies]
        return JsonResponse(results, safe=False)
    return JsonResponse({'message': 'No results found'}, status=404)


