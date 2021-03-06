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
from computing_environment.views import *
from allauth.account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('dashboard', dashboard, name='dashboard'),
    path('job/new', new_job, name='new_job'),
    path('job/<int:id>', show_job, name='show_job'),
    path('job/<int:id>/edit', edit_job, name='edit_job'),
    path('job/<int:id>/delete', delete_job, name='delete_job'),
    path('workers', show_workers, name="show_workers"),
    path('worker/<int:id>', show_worker, name='show_worker'),
    path('failed_jobs', show_failed, name='show_failed'),
    path('sub_job/<int:id>/delete', delete_sub_job, name='delete_sub_job'),
    path('profile', edit_profile, name='edit_profile'),
    path("download/<int:id>", download,  name="download"),
    path("download_all/<int:id>", download_all,  name="download_all"),

    ## allauth
    path('accounts/signup/<str:token>', view=custom_signup_view, name='account_signup'),
    path("accounts/login/", view=custom_login_view, name="account_login"),
    path("accounts/logout/", views.logout, name="account_logout"),
    path("accounts/password/change/", custom_password_change_view, name="account_change_password"),
    path("accounts/password/set/", views.password_set, name="account_set_password"),
    # password reset
    path("accounts/password/reset/", views.password_reset, name="account_reset_password"),
    path(
        "accounts/password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "accounts/password/reset/key/done/",
        views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),

    # django rest framework
    path("v1/jobs/job_to_do/", job_to_do, name="job_to_do_registered"),
    path("v1/jobs/job_to_do/<int:id>", job_to_do_registered, name="job_to_do"),
    path("v1/jobs/<int:id>/get_program", get_program, name="get_program"),
    path("v1/jobs/<int:id>/worker_report", worker_report, name="worker_report"),
    path("v1/jobs/<int:id>/send_result", send_result, name="send_result")
]

handler404 = error_404
handler403 = error_403
handler500 = error_500