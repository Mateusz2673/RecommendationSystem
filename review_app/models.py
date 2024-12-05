from django.db import models
from user_app.models import Users
from movie_app.models import Movies



# Create your models here.
class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, null=True, blank=True)
    rating = models.IntegerField()
    review_date = models.DateTimeField(auto_now=True)
    review_text = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'reviews'

    def get_star_rating(self):
        if self.rating is None:
            return {
                'full_stars': [],
                'half_stars': 0,
                'empty_stars': range(5)
            }
        full_stars = int(self.rating)
        decimal_part = self.rating - full_stars

        if 0.25 <= decimal_part < 0.75:
            half_stars = 1
        else:
            half_stars = 0

        empty_stars = 5 - full_stars - half_stars

        return {
            'full_stars': range(full_stars),
            'half_stars': half_stars,
            'empty_stars': range(empty_stars)
        }
    def __str__(self):
        return self.user.display_name + ' - ' + self.review_text

    @classmethod
    def get_reviews(cls):
        return cls.objects.all()

    @classmethod
    def get_reviews_head(cls):
        return cls.objects.all()[:5]

    @classmethod
    def get_review(cls, id):
        return cls.objects.get(pk=id)

    @classmethod
    def get_review_for_movie(cls, movie):
        return cls.objects.filter(movie=movie)

    @classmethod
    def get_latest_review(cls):
        return cls.objects.all().order_by('-review_date')[:3]

    @classmethod
    def query_reviews(cls, movie=None, author=None):
        if movie:
            return cls.objects.filter(movie=movie)
        if author:
            return cls.objects.filter(author__icontains=author)
        return cls.objects.all()

    @classmethod
    def sort_reviews(cls, movie, author, sort_by='rating'):
        reviews = cls.query_reviews(movie=movie, author=author)
        return reviews.order_by(sort_by)


class Moviecomments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Reviews, models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, null=True, blank=True)
    comment_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'moviecomments'

    def __str__(self):
        return self.review.movie.title + ' - ' + self.user.username

    def get_comments(self):
        return self.objects.all()

    def get_comment(self, id):
        return self.objects.get(pk=id)

    def query_comments(self, review=None, user=None):
        if review:
            return self.objects.filter(review=review)
        if user:
            return self.objects.filter(user=user)
        return self.objects.all()

    def sort_comments(self, review, user):
        comments = self.query_comments(review=review, user=user)
        return comments.order_by('date')

    @classmethod
    def get_comments_for_review(cls, review_id):
        return cls.objects.filter(review__id=review_id)