from django.urls import path

from YouTravel.trips.views import *

urlpatterns = [

    path('continents/', ContinentsListView.as_view(), name='list continents'),
    path('list/<int:pk>', trip_list, name='list trips'),
    path('my_list/', MyListTrips.as_view(), name='my list trips'),
    path('add_trip/', add_trip, name='add trip'),
    path('edit_trip/<int:pk>', edit_trip, name='edit trip'),
    path('delete_trip/<int:pk>', delete_trip, name='delete trip'),
    path('like_trip/<int:pk>', like_trip, name='like trip'),
    path('comment_trip/<int:pk>', comment_trip, name='comment trip'),
    path('delete_image/<int:pk>', delete_image, name='delete image'),

]
