from django.contrib.auth.models import AbstractUser

from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    profile_picture = models.ImageField()
    


class Account(models.Model):
    pass


class Transaction(models.Model):
    pass


class Order(models.Model):
    pass


class Product(models.Model):
    pass


class OrderItem(models.Model):
    pass

