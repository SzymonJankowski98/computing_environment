"""computing_environment URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from computing_environment.views import *
from allauth.account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('accounts/signup/<str:token>', view=custom_signup_view, name='account_signup'),
    path('accounts/', include('allauth.urls')),
    # path("accounts/login/", views.login, name="account_login"),
    # path("accounts/logout/", views.logout, name="account_logout"),
    # path(
    #     "accounts/password/change/",
    #     views.password_change,
    #     name="account_change_password",
    # ),
    # path("accounts/password/set/", views.password_set, name="account_set_password"),
    # # password reset
    # path("accounts/password/reset/", views.password_reset, name="account_reset_password"),
    # path(
    #     "accounts/password/reset/done/",
    #     views.password_reset_done,
    #     name="account_reset_password_done",
    # ),
    # re_path(
    #     r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
    #     views.password_reset_from_key,
    #     name="account_reset_password_from_key",
    # ),
    # path(
    #     "accounts/password/reset/key/done/",
    #     views.password_reset_from_key_done,
    #     name="account_reset_password_from_key_done",
    # ),
    
    re_path(r'.*', error_404, name='error_404')     # Don't add path below that
]