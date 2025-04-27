from django.db import models

class CrimeData(models.Model):
    city_code = models.IntegerField()
    crime_code = models.IntegerField()
    year = models.IntegerField()
    population = models.FloatField()
