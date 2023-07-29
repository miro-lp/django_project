from django.contrib import admin

from YouTravel.trips.models import Trip, Continent, TripImage


@admin.register(Trip)
class TripsAdmin(admin.ModelAdmin):
    list_display = ['name_trip', 'country_name', 'description', 'continent', 'publish_date', ]


@admin.register(Continent)
class TripsAdmin(admin.ModelAdmin):
    list_display = ['continent_name', 'description', 'image', ]


@admin.register(TripImage)
class TripsAdmin(admin.ModelAdmin):
    list_display = ['image', 'trip', ]
