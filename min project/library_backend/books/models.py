from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    rating = models.FloatField(default=4.0)

    def __str__(self):
        return self.title