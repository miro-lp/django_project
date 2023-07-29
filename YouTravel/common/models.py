from django.contrib.auth import get_user_model
from django.db import models

from YouTravel.accounts.models import TravelProfile
from YouTravel.trips.models import Trip

UserModel = get_user_model()


class Like(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        TravelProfile,
        related_name='from_user',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        TravelProfile,
        related_name='to_user',
        on_delete=models.CASCADE
    )
