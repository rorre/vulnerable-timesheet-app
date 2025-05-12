from django.urls import path

from cal.views import (
    approve_timesheet_view,
    cal_view,
    get_uploads_view,
    index_view,
    submit_timesheet_view,
    upload_file_view,
)


app_name = "cal"
urlpatterns = [
    path("", index_view, name="index"),
    path("<int:user_id>/", cal_view, name="user"),
    path("submit_timesheet/", submit_timesheet_view, name="submit_timesheet"),
    path("approve_timesheet/<int:timesheet_id>/", approve_timesheet_view, name="approve_timesheet"),
    path("upload_file/", upload_file_view, name="upload_file"),
    path("upload/<str:fname>/", get_uploads_view, name="get_uploads"),
]
