from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import TravelUserManager


class TravelUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False
    )
    USERNAME_FIELD = 'email'

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    object = TravelUserManager()


class TravelProfile(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15, blank=True)
    about_me = models.TextField(blank=True)
    motto = models.TextField(blank=True)

    profile_image = models.ImageField(
        upload_to='profiles',
        blank=True
    )
    user = models.OneToOneField(
        TravelUser,
        on_delete=models.CASCADE,
        primary_key=True
    )
    friends = models.ManyToManyField("TravelProfile", blank=True)

    def __str__(self):
        return self.user.email


from .signals import *
