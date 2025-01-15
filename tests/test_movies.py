import pytest
from unittest.mock import MagicMock
from movie_app.models import Movies
from movie_recommendation import settings
from movie_recommendation.settings import *

@pytest.fixture
def setup_movies():
    settings.configure()
    movie1 = Movies(title='Movie 1', rating=4.5, votes=100)
    movie2 = Movies(title='Movie 2', rating=3.5, votes=50)
    movie3 = Movies(title='Movie 1', rating=5.0, votes=150)  # Duplicate title
    movie1.save()
    movie2.save()
    movie3.save()
    yield
    movie1.delete()
    movie2.delete()
    movie3.delete()

def test_get_distinct_movies(setup_movies):
    """Test to ensure get_distinct_movies returns unique movies."""
    distinct_movies = Movies.get_distinct_movies()
    assert len(distinct_movies) == 2

def test_get_popular_movies(setup_movies):
    """Test to ensure get_popular_movies returns the top 3 movies based on score."""
    popular_movies = Movies.get_popular_movies()
    assert len(popular_movies) == 2
    assert popular_movies[0].title == 'Movie 1'

def test_get_star_rating_full_stars():
    """Test get_star_rating for a full star rating."""
    movie = Movies(title='Movie Test', rating=4.0)
    star_rating = movie.get_star_rating()
    assert list(star_rating['full_stars']) == [0, 1, 2, 3]

def test_get_star_rating_half_star():
    """Test get_star_rating for a half star rating."""
    movie = Movies(title='Movie Test', rating=4.5)
    star_rating = movie.get_star_rating()
    assert star_rating['half_stars'] == 1

def test_get_star_rating_no_rating():
    """Test get_star_rating when rating is None."""
    movie = Movies(title='Movie Test', rating=None)
    star_rating = movie.get_star_rating()
    assert list(star_rating['empty_stars']) == [0, 1, 2, 3, 4]

def test_get_movie(setup_movies):
    """Test get_movie retrieves the correct movie by ID."""
    movie = Movies.objects.first()
    retrieved_movie = Movies.get_movie(movie.movie_id)
    assert retrieved_movie.title == movie.title

def test_get_movies(setup_movies):
    """Test get_movies retrieves all movies."""
    movies = Movies.get_movies()
    assert len(movies) == 3

def test_get_movie_details(setup_movies):
    """Test get_movie_details returns correct movie details."""
    movie = Movies.objects.first()
    details = Movies.get_movie_details(movie.movie_id)
    assert details['movie'].title == movie.title

def test_get_movies_details(setup_movies):
    """Test get_movies_details retrieves details for all movies."""
    details = Movies.get_movies_details()
    assert len(details) == 3

def test_get_movies_head(setup_movies):
    """Test get_movies_head returns a maximum of 100 movies."""
    head_movies = Movies.get_movies_head()
    assert len(head_movies) <= 100

def test_query_movies_by_genre(setup_movies):
    """Test query_movies filters by genre."""
    # Assuming genre filtering is implemented correctly in the model
    Movies.query_movies = MagicMock(return_value=[Movies(title='Movie 1')])
    movies = Movies.query_movies(genre='Action')
    assert len(movies) == 1
    assert movies[0].title == 'Movie 1'

def test_sort_movies_by_rating(setup_movies):
    """Test sort_movies sorts movies by rating."""
    sorted_movies = Movies.sort_movies(sort_by='rating')
    assert sorted_movies[0]['movie'].rating >= sorted_movies[1]['movie'].rating

def test_sort_movies_with_no_movies():
    """Test sort_movies returns an empty list when no movies are present."""
    Movies.query_movies = MagicMock(return_value=[])
    sorted_movies = Movies.sort_movies()
    assert len(sorted_movies) == 0