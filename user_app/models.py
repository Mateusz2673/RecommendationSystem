from django.db import models
from movie_app.models import Movies
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    login = models.TextField(unique=True)
    password_hash = models.BinaryField()
    salt = models.BinaryField()
    display_name = models.TextField()
    user_role = models.CharField(default='user')
    email = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    surname = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.login

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


    @property
    def password(self):
        return bytes(self.password_hash).decode()

    def set_password(self, raw_password):
        hashed_password = make_password(raw_password)
        self.password_hash = hashed_password.encode()
        self.save()

    @property
    def last_login(self):
        return None

    @last_login.setter
    def set_last_login(self, last_login):
        pass

    @property
    def groups(self):
        return QuerySet()

    @groups.setter
    def set_groups(self, groups):
        pass

    @property
    def user_permissions(self):
        return QuerySet()

    @user_permissions.setter
    def user_permissions(self, value):
        pass

    def save(self, *args, **kwargs):
        self.display_name = f"{self.surname} {self.first_name}"
        super().save(*args, **kwargs)

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

    @classmethod
    def get_users_head(cls):
        return cls.objects.all()[:5]

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
    movie = models.ForeignKey(Movies, models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'favouritemovies'