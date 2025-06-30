from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Collector(AbstractUser):
    bio = models.CharField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def total_items(self):
        return self.coins.count() + self.banknotes.count()

    # Для цікавості додав систему рівнів на сайті)
    def level(self):
        total = self.total_items()
        if total < 50:
            return "Beginner"
        elif total < 90:
            return "The collector 🎖️"
        elif total < 150:
            return "Silver Seeker 🎖️"
        elif total < 300:
            return "Elite collector 📚"
        elif total < 500:
            return "Collector of history 🕰️"
        else:
            return "Legendary collector ✨"

class Coin(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    denomination = models.CharField(max_length=25)
    material = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    tirage = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    image = models.ImageField(upload_to="coins/", blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE, related_name="coins")

    def __str__(self):
        return f"Coin {self.name} (Country:{self.country} Year: {self.year})"

    def get_absolute_url(self):
        return reverse("items:coin-detail", args=[str(self.id)])

class Banknote(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    value = models.CharField(max_length=65)
    tirage = models.CharField(max_length=65, default="Unknown", blank=True, null=True)
    image = models.ImageField(upload_to="banknotes/", blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE, related_name="banknotes")

    def __str__(self):
        return f"Banknote {self.name} (Country:{self.country} Year: {self.year})"

    def get_absolute_url(self):
        return reverse("items:banknote-detail", args=[str(self.id)])

class Collection(models.Model):
    cover = models.ImageField(upload_to="collections/covers/", blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=100, null=True, blank=True)
    coins = models.ManyToManyField(Coin)
    banknotes = models.ManyToManyField(Banknote)

    def __str__(self):
        return f"Collection {self.name} by {self.owner.username}"

    def get_absolute_url(self):
        return reverse("items:collection-detail", args=[str(self.id)])
