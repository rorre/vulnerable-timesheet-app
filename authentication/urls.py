from django.urls import path
from authentication.views import login_view, logout_view, register_view

app_name = "authentication"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
