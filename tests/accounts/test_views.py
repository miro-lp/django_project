from django.contrib.auth import get_user_model

from django.test import TestCase, Client
from django.urls import reverse, resolve

from YouTravel.accounts.models import TravelProfile
from YouTravel.common.models import FriendRequest

UserModel = get_user_model()


class AccountsViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.object.create_user(email='miro_lp@abv.bg', password='12345678')

    def test_signup_GET(self):
        response = self.client.get(reverse('sign up'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_POST(self):
        response = self.client.post(reverse('sign up'), data={
            'email': 'miro_lp1@abv.bg',
            'password1': '1q!Q2w@W',
            'password2': '1q!Q2w@W'
        })
        logged_in = self.client.login(email='miro_lp1@abv.bg', password='1q!Q2w@W')

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('profile details'), response['Location'])
        self.assertTrue(logged_in)

    def test_login_GET(self):
        response = self.client.get(reverse('sign in'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_when_user_sign_in_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTrue(response.context['user'].is_active)

    def test_login_POST__user_exist_redirect_index(self):
        response = self.client.post(reverse('sign in'), data={
            'email': 'miro_lp@abv.bg',
            'password': '12345678'
        })
        logged_in = self.client.login(email='miro_lp@abv.bg', password='12345678')

        self.assertEquals(302, response.status_code)
        self.assertEquals(reverse('index'), response['Location'])
        self.assertTrue(logged_in)

    def test_login_POST__user_not_exist(self):
        response = self.client.post(reverse('sign in'), data={
            'email': 'miro_lp1@abv.bg',
            'password': '12345678'
        })
        logged_in = self.client.login(email='miro_lp1@abv.bg', password='12345678')

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(logged_in)

    def test_profile_details_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile details'))
        profile = response.context['profile']

        self.assertEquals(200, response.status_code)
        self.assertEquals(self.user.id, profile.user_id)
        self.assertTemplateUsed(response, 'accounts/profile_details.html')

    def test_profile_details_edit_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile edit'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_profile_details_edit_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('profile edit'), data={
            'first_name': 'Pesho'
        })

        self.assertEquals(302, response.status_code)

        profile = TravelProfile.objects.get(user_id=self.user.id)
        self.assertEquals('Pesho', profile.first_name)

    def test_TravelersList_GET(self):
        self.client.force_login(self.user)
        UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')

        response = self.client.get(reverse('profiles list'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/profiles_list.html')
        self.assertEquals(1, len(response.context['travelprofile_list']))

    def test_send_friend_request_if_not_exist(self):
        self.client.force_login(self.user)
        user1 = UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')
        self.client.get(reverse('send friend request', kwargs={'pk': user1.id}))
        friends_request = FriendRequest.objects.all()

        self.assertEqual(1, len(friends_request))

    def test_send_friend_request_if_exist(self):
        self.client.force_login(self.user)
        user1 = UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')
        profile = TravelProfile.objects.get(user_id=self.user.id)
        profile1 = TravelProfile.objects.get(user_id=user1.id)
        FriendRequest.objects.create(from_user=profile, to_user=profile1)
        friends_request = FriendRequest.objects.filter(from_user=profile.user_id, to_user=profile1.user_id)

        self.client.get(reverse('send friend request', kwargs={'pk': user1.id}))

        self.assertEqual(1, len(friends_request))

    # def test_accept_friend_request(self):
    #     self.client.force_login(self.user)
    #     user2 = UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')
    #     profile = TravelProfile.objects.get(user_id=self.user.id)
    #     profile2 = TravelProfile.objects.get(user_id=user2.id)
    #     FriendRequest.objects.create(from_user=profile2, to_user=profile)
    #     self.client.get(reverse('accept friend request', kwargs={'pk': self.user.id}))
    #     friends_request = FriendRequest.objects.all()
    #
    #     self.assertEqual(0, len(friends_request))

    def test_ShowFriendRequests_null_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('show friend request'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/show_friend_requests.html')
        self.assertEquals(0, len(response.context['friendrequest_list']))

    def test_ShowFriendRequests_not_null_GET(self):
        self.client.force_login(self.user)
        profile = TravelProfile.objects.get(user_id=self.user.id)
        user1 = UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')
        profile1 = TravelProfile.objects.get(user_id=user1.id)
        FriendRequest.objects.create(from_user=profile1, to_user=profile)

        response = self.client.get(reverse('show friend request'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/show_friend_requests.html')
        self.assertEquals(1, len(response.context['friendrequest_list']))

    def test_ShowMyFriends_null_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('friends list'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/friends_list.html')
        self.assertEquals(0, len(response.context['travelprofile_list']))

    def test_ShowMyFriends_not_null_GET(self):
        self.client.force_login(self.user)
        profile = TravelProfile.objects.get(user_id=self.user.id)
        user1 = UserModel.object.create_user(email='miro1_lp@abv.bg', password='123456781')
        profile1 = TravelProfile.objects.get(user_id=user1.id)
        profile1.friends.add(profile)
        profile.friends.add(profile1)

        response = self.client.get(reverse('friends list'))

        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'accounts/friends_list.html')
        self.assertEquals(len(response.context['travelprofile_list']), 1)
