from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('tracker.urls')),
]

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()

try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')