from django.db import models

# Create your models here.

class authors(models.Model):
    id = models.CharField(max_length=64)
    headline = models.CharField(max_length=64)
    category = models.CharField(choices=[()])
    author = models.ForeignKey(stories, null=True)
    date = models.DateField()
    details = models.CharField(max_length=512)
    

class stories(models.Model):
    pass


