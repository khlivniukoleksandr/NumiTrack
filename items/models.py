from django.contrib.auth.models import AbstractUser
from django.db import models


class Collector(AbstractUser):
    bio = models.CharField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)


class Coin(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    denomination = models.CharField(max_length=25)
    material = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    tirage = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    image = models.ImageField(upload_to="coins/", blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coin {self.name} (Country:{self.country} Year: {self.year})"

class Banknote(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    value = models.CharField(max_length=65)
    tirage = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    image = models.ImageField(upload_to="banknotes/", blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE)

    def __str__(self):
        return f"Banknote {self.name} (Country:{self.country} Year: {self.year})"


class Collection(models.Model):
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=100, null=True, blank=True)
    coins = models.ManyToManyField(Coin)
    banknotes = models.ManyToManyField(Banknote)

    def __str__(self):
        return f"Collection {self.name} by {self.owner.username}"
