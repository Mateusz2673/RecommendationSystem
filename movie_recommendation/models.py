from django.db.models import Value, QuerySet

from movie_app.models import Movies, Genredetails, Genre, Directors
from review_app.models import Reviews
from user_app.models import Users


class MovieRecommender:
    # How many stars are considered a positive review
    rating_threshold: int = 4
    # How many recent reviews/favourites to consider for the algorithm
    __search_limit: int = 3

    def __init__(self, count: int = 6):
        super().__init__()
        self.count = count

    def movie_recommendations(
            self, movie: Movies, use_content: bool = True, use_collaborative: bool = True
    ) -> Movies:
        """
        Combines content-based and collaborative filtering recommendations based on parameters.
        :param movie: Movies instance
        :param use_content: Include content-based recommendations
        :param use_collaborative: Include collaborative filtering recommendations
        :return: Movies queryset
        """
        recommendations = []
        print(movie)
        print(type(movie))
        if use_collaborative:
            collaborative_recommendations = self.collaborative_recommendations(movie)
            collaborative_recommendations = collaborative_recommendations.annotate(
                custom_order=Value(1)
            )
            recommendations.append(collaborative_recommendations)
            print(f"collaborative_recommendations: {collaborative_recommendations}")
        if use_content:
            content_recommendations = self.content_based_recommendations(movie)
            content_recommendations = content_recommendations.annotate(
                custom_order=Value(2)
            )
            recommendations.append(content_recommendations)
            print(f"content_recommendations: {content_recommendations}")
        if recommendations:
            # Union all recommendations and order
            movies = (
                recommendations[0].union(*recommendations[1:])

            )
            print(f"rekomendacje: {movies}")
            return movies[:self.count]

        return Movies.objects.none()

    def user_recommendations(self, user: Users) -> Movies:
        """
        Usage:
        some_user: Users = ...
        recommended_movies: Movies = MovieRecommender(count=50).user_recommendations(some_user)
        """
        return self.__from_recent_positive_reviews(user=user)

    def __from_positive_reviews(self, movie: Movies) -> Movies:
        if not isinstance(movie, (Movies, QuerySet)):
            raise ValueError("Expected 'movie' to be an instance of Movies or QuerySet.")

        print(type(movie))
        print(movie)

        positive_reviews = Reviews.objects.filter(
            movie__in=movie, rating__gte=MovieRecommender.rating_threshold
        )
        print("Positive reviews:", positive_reviews)

        recommending_users = positive_reviews.values_list("user", flat=True)
        print("Recommending users:", recommending_users)
        users_recommend_movies = (
            Reviews.objects.filter(
                user__in=recommending_users,
                rating__gte=MovieRecommender.rating_threshold,
            )
            #.exclude(movie__in=movie)
            .values_list("movie", flat=True)
        )
        print("Movies recommended by users:", users_recommend_movies)
        movies = Movies.objects.filter(movie_id__in=users_recommend_movies).distinct()
        print("Final collaborative recommendations:", movies)
        return movies

    def __popular_in_genres(self, movie: Movies) -> Movies:
        genres = Genredetails.objects.filter(genre__movie__in=movie)
        movies = (
            Movies.objects.filter(
                genre__genre__in=genres, rating__gte=MovieRecommender.rating_threshold
            )
            .exclude(movie_id__in=[movie[0].movie_id])
            .distinct()
        )
        return movies

    def __from_recent_positive_reviews(self, user: Users) -> Movies:
        limit_reviews = 10
        recent_reviews = Reviews.objects.filter(
            user=user, rating__gte=MovieRecommender.rating_threshold
        )[:limit_reviews]
        liked_movies = Movies.objects.filter(
            movie_id__in=recent_reviews.values_list("movie", flat=True)
        )


        return self.movie_recommendations(liked_movies)

    def content_based_recommendations(self, movie: Movies, count: int = 6) -> Movies:
        genre_recommendations = self.__popular_in_genres(movie=movie)
        return genre_recommendations

    def collaborative_recommendations(self, movie: Movies, count: int = 6) -> Movies:
        smart_recommendations = self.__from_positive_reviews(movie=movie)
        return smart_recommendations
