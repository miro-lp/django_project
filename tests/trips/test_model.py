from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from YouTravel.trips.models import Continent, Trip

UserModel = get_user_model()


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.africa = Continent.objects.create(continent_name='Africa', description='Test',
                                               image='/medial_files/test.jpeg')
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')

    def test_model_trip_valid(self):
        self.client.force_login(self.user)

        trip = Trip(name_trip='Test trip',
                    country_name='Test country',
                    description='It is a test',
                    continent=self.africa,
                    user=self.user)
        trip.full_clean()

        self.assertTrue(trip)

    def test_model_trip_invalid_lower_alpha_name(self):
        self.client.force_login(self.user)

        trip = Trip(name_trip='te',
                    country_name='Test country',
                    description='It is a test',
                    continent=self.africa,
                    user=self.user)

        self.assertRaises(ValidationError, trip.full_clean)
