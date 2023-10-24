from django.conf.urls import include
from django.urls import path, re_path
from users.views import dashboard

urlpatterns = [
    re_path(r"^dashboard/", dashboard, name="dashboard"),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
]