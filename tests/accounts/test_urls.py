from django.test import SimpleTestCase
from django.urls import reverse, resolve
from YouTravel.accounts.views import *


class TestUrls(SimpleTestCase):

    def test_sign_in_url(self):
        url = reverse('sign in')
        self.assertEqual(sign_in_user, resolve(url).func)

    def test_sign_up_url(self):
        url = reverse('sign up')
        self.assertEqual(sign_up_user, resolve(url).func)

    def test_sign_out_url(self):
        url = reverse('sign out')
        self.assertEqual(sign_out_user, resolve(url).func)

    def test_profile_details_url(self):
        url = reverse('profile details')
        self.assertEqual(ProfileDetails, resolve(url).func.view_class)

    def test_profile_edit(self):
        url = reverse('profile edit')
        self.assertEqual(profile_edit, resolve(url).func)

    def test_profile_edit(self):
        url = reverse('profiles list')
        self.assertEqual(TravelersListView, resolve(url).func.view_class)

    def test_send_friend_request(self):
        url = reverse('send friend request', kwargs={'pk': int()})
        self.assertEqual(send_friend_request, resolve(url).func)

    def test_show_friend_request(self):
        url = reverse('show friend request')
        self.assertEqual(ShowFriendRequests, resolve(url).func.view_class)

    def test_accept_friend_request(self):
        url = reverse('accept friend request', kwargs={'pk': int()})
        self.assertEqual(accept_friend_request, resolve(url).func)

    def test_show_friends(self):
        url = reverse('friends list')
        self.assertEqual(ShowMyFriends, resolve(url).func.view_class)
