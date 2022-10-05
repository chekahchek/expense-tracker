from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='tracker'

urlpatterns = [
    path('', views.HomeView.as_view(), name='main'),
    path('trip', views.TripListView.as_view(), name='trip_list'),
    path('trip/<int:pk>/edit', views.TripUpdate.as_view(), name='trip_update'),
    path('trip/<int:pk>/delete', views.TripDelete.as_view(), name='trip_delete'),
    path('trip/<int:pk>', views.TripDetaiView.as_view(), name='trip_detail'),
    path('trip/<int:pk>/expense', views.TripExpense.as_view(), name='trip_expense'),
    path('trip/<int:pk>/expense/edit/<int:expense_id>', views.TripExpenseUpdate.as_view(), name='trip_expense_update'),
    path('trip/<int:pk>/expense/delete/<int:expense_id>', views.TripExpenseDelete.as_view(), name='trip_expense_delete'),
    path('trip/<int:pk>/blog', views.TripBlog.as_view(), name='trip_blog'),
    path('trip/<int:pk>/share', views.ShareTripView.as_view(), name='share_trip'),
    path('testing', views.Debugging.as_view(), name='debug'),
]