from django.db import models
from django.contrib.auth.models import AbstractUser

class File(models.Model):
    file = models.FileField()

    def __int__(self):
        return self.id


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')
    register_time = models.DateTimeField()
    address = models.CharField(max_length=255, default='')

    def __int__(self):
        return self.id


class Popcorn(models.Model):
    name = models.CharField(unique=True, max_length=255, default='')
    size = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='')
    popularity = models.IntegerField(default=0)
    price = models.IntegerField(default=10000)
    photo = models.ForeignKey(File, on_delete=models.CASCADE)

    def __int__(self):
        return self.id


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    popcorn = models.ForeignKey(Popcorn, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
