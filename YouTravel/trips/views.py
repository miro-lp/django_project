from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect


from YouTravel.common.forms import CommentForm
from YouTravel.common.models import Like, Comment
from YouTravel.trips.forms import TripForm, TripImageFrom
from YouTravel.trips.models import Trip, Continent, TripImage


class ContinentsListView(ListView):
    model = Continent
    template_name = 'trips/continents_list.html'
    ordering = ["continent_name"]


def trip_list(request, pk):
    trips = Trip.objects.all().filter(continent_id=pk)
    is_liked_by_user = {}
    comments = Comment.objects.all()
    for trip in trips:
        trip.likes_count = trip.like_set.count()
        is_liked_by_user[trip.id] = trip.like_set.filter(user_id=request.user.id).exists()

    context = {
        'trips': trips,
        'is_liked_by_user': is_liked_by_user,
        'comments': comments,
        'comment_form': CommentForm(),
    }
    return render(request, 'trips/list_trips.html', context)


# @login_required
# def my_trip_list(request, pk):
#     my_trips = Trip.objects.all().filter(user_id=pk)
#     context = {'my_trips': my_trips,
#                }
#     return render(request, 'trips/my_list_trips.html', context)


class MyListTrips(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/my_list_trips.html'
    paginate_by = 3
    context_object_name = "my_trips"

    def get_queryset(self):
        return Trip.objects.all().filter(user=self.request.user)


@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        form_image = TripImageFrom(request.POST, request.FILES)
        if form.is_valid() and form_image.is_valid():
            trip = form.save(commit=False)
            image = form_image.save(commit=False)
            trip.user = request.user
            trip.save()
            image.trip = Trip.objects.get(id=trip.id)
            image.save()
            return redirect('profile details')

    else:
        form = TripForm()
        form_image = TripImageFrom()
    context = {
        'form': form,
        'form_image': form_image
    }
    return render(request, 'trips/add_trip.html', context)


@login_required
def edit_trip(request, pk):
    trip = Trip.objects.get(id=pk)
    images = TripImage.objects.filter(trip_id=trip.id)
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        form_image = TripImageFrom(request.POST, request.FILES)
        if form.is_valid() and form_image.is_valid():
            trip = form.save(commit=False)
            image = form_image.save(commit=False)
            trip.user = request.user
            trip.save()
            image.trip = Trip.objects.get(id=trip.id)
            image.save()
            return redirect('my list trips')
    else:
        form = TripForm(instance=trip)
        form_image = TripImageFrom()
    context = {
        'form': form,
        'form_image': form_image,
        'trip': trip,
        'images': images
    }
    return render(request, 'trips/edit_trip.html', context)


@login_required
def delete_image(request, pk):
    image = TripImage.objects.get(pk=pk)
    trip = Trip.objects.get(id=image.trip_id)
    images = TripImage.objects.filter(trip_id=trip.id)
    image.delete()
    form = TripForm(instance=trip)
    form_image = TripImageFrom()
    context = {
        'form': form,
        'form_image': form_image,
        'trip': trip,
        'images': images
    }
    return render(request, 'trips/edit_trip.html', context)


@login_required
def delete_trip(request, pk):
    trip = Trip.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        trip.delete()
        return redirect('my list trips')
    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'trips/delete_trip.html', context)


@login_required
def like_trip(request, pk):
    trip = Trip.objects.get(pk=pk)
    is_liked_by_user = trip.like_set.filter(user_id=request.user.id).first()
    if is_liked_by_user:
        is_liked_by_user.delete()
    else:
        like = Like(trip=trip, user=request.user, )
        like.save()
    return redirect('list trips', trip.continent_id)


@login_required
def comment_trip(request, pk):
    trip = Trip.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(
            comment=form.cleaned_data['text'],
            trip=trip,
            user=request.user
        )
        comment.save()
    return redirect('list trips', trip.continent_id)
