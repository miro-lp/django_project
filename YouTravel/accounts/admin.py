from django.contrib import admin

# Register your models here.
from YouTravel.accounts.models import TravelProfile, TravelUser


@admin.register(TravelUser)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff', ]


@admin.register(TravelProfile)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', ]
