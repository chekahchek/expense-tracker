from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('', include('tracker.urls')),
]
