from django.urls import path

from YouTravel.accounts.views import *

urlpatterns = [
    path('sign_in/', sign_in_user, name='sign in'),
    path('sign_up/', sign_up_user, name='sign up'),
    path('sign_out/', sign_out_user, name='sign out'),
    path('profile/', ProfileDetails.as_view(), name='profile details'),
    path('profile_edit/', profile_edit, name='profile edit'),
    path('profiles/', TravelersListView.as_view(), name='profiles list'),
    path('request/<int:pk>', send_friend_request, name='send friend request'),
    path('show_request/', ShowFriendRequests.as_view(), name='show friend request'),
    path('accept_request/<int:pk>', accept_friend_request, name='accept friend request'),
    path('show_friends/', ShowMyFriends.as_view(), name='friends list'),
]
