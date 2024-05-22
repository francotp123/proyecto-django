from django.db import models

# Create your models here.
class Influencers(models.Model):
    username = models.CharField(max_length=200)
    rank = models.IntegerField()
    category = models.CharField(max_length=200)
    followers = models.IntegerField()
    audience_country = models.CharField(max_length=200)
    aut_eng = models.IntegerField()
    avg_eng = models.IntegerField()

    