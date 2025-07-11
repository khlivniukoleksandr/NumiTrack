from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
import cloudinary.uploader

class Collector(AbstractUser):
    bio = models.CharField(max_length=500, blank=True, null=True)
    avatar = CloudinaryField('image', blank=True, null=True)

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
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    denomination = models.CharField(max_length=15)
    material = models.CharField(max_length=30, default="Unknown", blank=True, null=True)
    tirage = models.CharField(max_length=20, default="Unknown", blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE, related_name="coins")

    def __str__(self):
        return f"Coin {self.name} (Country:{self.country} Year: {self.year})"

    def get_absolute_url(self):
        return reverse("items:coin-detail", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        try:
            if self.image and hasattr(self.image, 'public_id'):
                public_id = self.image.public_id
                cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Cloudinary deletion error: {e}")
        super().delete(*args, **kwargs)


class Banknote(models.Model):
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    value = models.CharField(max_length=25)
    tirage = models.CharField(max_length=15, default="Unknown", blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE, related_name="banknotes")


    def __str__(self):
        return f"Banknote {self.name} (Country:{self.country} Year: {self.year})"

    def get_absolute_url(self):
        return reverse("items:banknote-detail", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        try:
            if self.image and hasattr(self.image, 'public_id'):
                cloudinary.uploader.destroy(self.image.public_id)
        except Exception as e:
            print(f"Cloudinary deletion error: {e}")
        super().delete(*args, **kwargs)


class Collection(models.Model):
    cover = CloudinaryField('image', blank=True, null=True)
    owner = models.ForeignKey(Collector, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=100)
    coins = models.ManyToManyField(Coin)
    banknotes = models.ManyToManyField(Banknote)

    def __str__(self):
        return f"Collection {self.name} by {self.owner.username}"

    def get_absolute_url(self):
        return reverse("items:collection-detail", args=[str(self.id)])

    def delete(self, *args, **kwargs):
        try:
            if self.cover and hasattr(self.cover, 'public_id'):
                cloudinary.uploader.destroy(self.cover.public_id)
        except Exception as e:
            print(f"Cloudinary deletion error: {e}")
        super().delete(*args, **kwargs)


