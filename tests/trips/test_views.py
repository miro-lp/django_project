from os.path import join

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, Client
from django.urls import reverse, resolve

from YouTravel.common.models import Comment, Like
from YouTravel.trips.models import Continent, Trip

UserModel = get_user_model()


class AccountsViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')
        self.africa = Continent.objects.create(continent_name='Africa', description='Test',
                                               image='/medial_files/test.jpeg')

    def test_continents_listT_with_1_continent_GET(self):
        response = self.client.get(reverse('list continents'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/continents_list.html')
        self.assertEquals(1, len(response.context['continent_list']))

    def test_trips_list_no_trips_GET(self):
        response = self.client.get(reverse('list trips', kwargs={'pk': self.africa.id}))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/list_trips.html')
        self.assertEquals(0, len(response.context['trips']))

    def test_trips_list_with_comment_like_GET(self):
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        Comment.objects.create(comment='Test comment',
                               user=self.user,
                               trip=trip)
        Like.objects.create(trip=trip,
                            user=self.user)

        response = self.client.get(reverse('list trips', kwargs={'pk': self.africa.id}))

        self.assertEquals(200, response.status_code, )
        self.assertTemplateUsed(response, 'trips/list_trips.html')
        self.assertEquals(1, len(response.context['trips']))
        self.assertEquals(1, len(response.context['comments']))
        self.assertTrue(response.context['is_liked_by_user'])

    def test_my_trips_list_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my list trips'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/my_list_trips.html')
        self.assertEquals(0, len(response.context['my_trips']))

    def test_add_trip_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add trip'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/add_trip.html')

    def test_add_trip_invalid_form_POST(self):
        image_path = join(settings.BASE_DIR, 'tests', 'trips', 'images', 'test.jpg')
        image = SimpleUploadedFile(name='test_image.jpg',
                                   content=open(image_path, 'rb').read(),
                                   content_type='image/jpeg')
        self.client.force_login(self.user)
        response = self.client.post(reverse('add trip'), data={'name_trip': 'Test trip',
                                                               'country_name': 'Test country',
                                                               'description': 'It is a test',
                                                               'continent': {'Africa': self.africa},
                                                               'image': image, })

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/add_trip.html')

    def test_edit_trip_GET(self):
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        self.client.force_login(self.user)

        response = self.client.get(reverse('edit trip', kwargs={'pk': trip.id}))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/edit_trip.html')

    def test_delete_trip_GET(self):
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        self.client.force_login(self.user)

        response = self.client.get(reverse('delete trip', kwargs={'pk': trip.id}))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'trips/delete_trip.html')

    def test_delete_trip_POST(self):
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        self.client.force_login(self.user)

        response = self.client.post(reverse('delete trip', kwargs={'pk': trip.id}))

        self.assertEquals(302, response.status_code)
        self.assertEquals(0, len(Trip.objects.all()))
        self.assertEquals(reverse('my list trips'), response['Location'])

    def test_like_trip_when_is_liked(self):
        self.client.force_login(self.user)
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        Like.objects.create(trip=trip,
                            user=self.user)
        response = self.client.get(reverse('like trip', kwargs={'pk': trip.id}))
        is_like_exist = Like.objects.filter(user_id=self.user.id, trip_id=trip.id)

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('list trips', kwargs={'pk': trip.continent_id}), response['Location'])
        self.assertEquals(0, len(is_like_exist))

    def test_like_trip_when_not_is_liked(self):
        self.client.force_login(self.user)
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)
        response = self.client.get(reverse('like trip', kwargs={'pk': trip.id}))
        is_like_exist = Like.objects.filter(user_id=self.user.id, trip_id=trip.id)

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('list trips', kwargs={'pk': trip.continent_id}), response['Location'])
        self.assertEquals(1, len(is_like_exist))

    def test_comment_trip_POST(self):
        self.client.force_login(self.user)
        trip = Trip.objects.create(name_trip='Test_trip',
                                   country_name='Test_country',
                                   description='It is a test',
                                   continent=self.africa,
                                   user=self.user)

        response = self.client.post(reverse('comment trip', kwargs={'pk': trip.id}), data={'text': 'Test comment'})
        comment = Comment.objects.filter(trip_id=trip.id, user_id=self.user.id)

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('list trips', kwargs={'pk': trip.continent_id}), response['Location'])
        self.assertEquals(1, len(comment))
