from django.urls import path
from administrator.views import index_view, set_manager_view

app_name = "administrator"
urlpatterns = [
    path("", index_view, name="index"),
    path("set_manager/<int:user_id>", set_manager_view, name="set_manager"),
]
