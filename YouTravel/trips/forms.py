from django import forms

from YouTravel.core.forms import BootstrapFormMixin
from YouTravel.trips.models import Trip, TripImage


class TripImageFrom(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = TripImage
        fields = ('image',)


class TripForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ('user',)
        fields = '__all__'
