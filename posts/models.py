from django.db import models
from django.urls import reverse

class Post(models.Model):                             # Inheritance
    title = models.CharField(max_length=128)          # Composition
    subtitle = models.CharField(max_length=256)       # Composition
    body = models.TextField()                         # Composition
    created_on = models.DateTimeField(auto_now=True)  # Composition
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", args=[self.id])