from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from YouTravel.trips.forms import TripForm
from YouTravel.trips.models import Continent

UserModel = get_user_model()


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.africa = Continent.objects.create(continent_name='Africa', description='Test',
                                               image='/medial_files/test.jpeg')
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')

    def test_trip_form_widget_class(self):
        form = TripForm(data={'name_trip': 'Test trip',
                              'country_name': 'Test country',
                              'description': 'It is a test',
                              'continent': self.africa,
                              })

        self.assertTrue(form.is_valid())
        self.assertEquals('form-control', form.fields['name_trip'].widget.attrs['class'])
        self.assertEquals('form-control', form.fields['country_name'].widget.attrs['class'])
        self.assertEquals('form-control', form.fields['description'].widget.attrs['class'])
