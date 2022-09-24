from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='tracker'

urlpatterns = [
    path('', views.HomeView.as_view(), name='main'),
    path('trip', views.TripListView.as_view(), name='trip_list'),
    path('trip/create', views.CreateTripView.as_view(), name='create_trip'),
    path('trip/<int:pk>', views.TripDetaiView.as_view(), name='trip_detail'),
    path('trip/<int:pk>/share', views.ShareTripView.as_view(), name='share_trip'),
    path('testing', views.Debugging.as_view(), name='debug'),
]