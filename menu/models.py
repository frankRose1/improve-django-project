from django.db import models
from django.utils import timezone
from django.urls import reverse


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(
            default=timezone.now)
    expiration_date = models.DateTimeField(
            blank=True, null=True)
    
    class Meta:
        ordering = ['expiration_date',]

    def __str__(self):
        return self.season

    def get_absolute_url(self):
        return reverse('menu:detail', kwargs={'pk': self.id})


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
