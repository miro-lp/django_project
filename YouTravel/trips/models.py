from django.contrib.auth import get_user_model
from django.db import models

from YouTravel.trips.validators import *

UserModel = get_user_model()


class Continent(models.Model):
    CONTINENTS_CHOICE = [('Africa', 'Africa'),
                         ('Asia', 'Asia'),
                         ('Australia', 'Australia'),
                         ('Europe', 'Europe'),
                         ('North America', 'North America'),
                         ('South America', 'South America'),
                         ]

    continent_name = models.CharField(max_length=15, choices=CONTINENTS_CHOICE)
    description = models.TextField()
    image = models.ImageField(upload_to='continents')

    def __str__(self):
        return self.continent_name


class Trip(models.Model):
    name_trip = models.CharField(max_length=15,
                                 validators=(is_title_start_alpha,
                                             is_title_start_capitalized,
                                             is_title_length_less))
    country_name = models.CharField(max_length=15)
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    continent = models.ForeignKey(
        Continent,
        on_delete=models.CASCADE,

    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name_trip


class TripImage(models.Model):
    image = models.ImageField(upload_to='trip_images')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
