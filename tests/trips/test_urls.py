from django.test import SimpleTestCase
from django.urls import reverse, resolve
from YouTravel.trips.views import *


class TestTripsUrls(SimpleTestCase):

    def test_list_continents_url(self):
        url = reverse('list continents')
        self.assertEqual(ContinentsListView, resolve(url).func.view_class)

    def test_list_trips_url(self):
        url = reverse('list trips', kwargs={'pk': int()})
        self.assertEqual(trip_list, resolve(url).func)

    def test_list_my_trips_url(self):
        url = reverse('my list trips')
        self.assertEqual(MyListTrips, resolve(url).func.view_class)

    def test_add_trip_url(self):
        url = reverse('add trip')
        self.assertEqual(add_trip, resolve(url).func)

    def test_edit_trip_url(self):
        url = reverse('edit trip', kwargs={'pk': int()})
        self.assertEqual(edit_trip, resolve(url).func)

    def test_delete_trip_url(self):
        url = reverse('delete trip', kwargs={'pk': int()})
        self.assertEqual(delete_trip, resolve(url).func)

    def test_like_trip_url(self):
        url = reverse('like trip', kwargs={'pk': int()})
        self.assertEqual(like_trip, resolve(url).func)

    def test_comment_trip_url(self):
        url = reverse('comment trip', kwargs={'pk': int()})
        self.assertEqual(comment_trip, resolve(url).func)

    def test_delete_image_url(self):
        url = reverse('delete image', kwargs={'pk': int()})
        self.assertEqual(delete_image, resolve(url).func)
