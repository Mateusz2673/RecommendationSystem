from django.db import models
from movie_app.models import Movies
from django.contrib.auth.hashers import check_password as django_check_password


# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.TextField(unique=True)
    password_hash = models.BinaryField()
    salt = models.BinaryField()
    display_name = models.TextField()
    user_role = models.CharField(default='user')

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.display_name
    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True

    def check_password(self, raw_password):
        password_hash = self.password_hash.tobytes().decode()
        return django_check_password(raw_password, password_hash)


    @classmethod
    def get_user(cls, id):
        return cls.objects.get(pk=id)

    @classmethod
    def get_users(cls):
        return cls.objects.all()

    @classmethod
    def get_users_head(cls):
        return cls.objects.all()[:5]

    def get_user_favorite_movies(self):
        return self.favouritemovies_set.all()

    def get_user_reviews(self):
        return self.reviews_set.all()

    def get_user_comments(self):
        return self.comments.all()

    @classmethod
    def query_users(cls, login=None, display_name=None):
        if login:
            return cls.objects.filter(username__icontains=login)
        if display_name:
            return cls.objects.filter(email__icontains=display_name)
        return cls.objects.all()

    @classmethod
    def sort_users(cls, username, email, sort_by='date_joined'):
        users = cls.query_users(username=username, email=email)
        return users.order_by(sort_by)


class Favouritemovies(models.Model):
    favourite_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favouritemovies'
