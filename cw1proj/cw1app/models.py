from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Author(AbstractUser):
    class Meta:
        db_table = "Authors"

    author_name = models.CharField(max_length=50, null=False)

class Story(models.Model):
    class Meta:
        db_table = "Stories"
    key = models.CharField(primary_key=True, max_length=64, null=False)
    headline = models.CharField(max_length=64, null=False)
    category = models.CharField(max_length=10, choices=[('pol', 'politics'), ('art', 'art news'), ('tech', 'tech news'),('trivia', 'trivial news')], null=False)
    region = models.CharField(max_length=10, choices=[('uk', 'united kingdom'), ('eu', 'european union'), ('w', 'world')], null=False, default='w')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)
    details = models.CharField(max_length=512, null=False)