import json
from cal.models import Timesheet
import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpRequest, HttpResponse
from django.contrib import messages

from authentication.models import Employee
import os


def get_employee_timesheet_for_month(employee: Employee, dt: datetime.date):
    """
    Get the timesheet for a specific month.
    :param employee: Employee object
    :param dt: datetime object
    :return: List of timesheets for the month
    """
    start_date = dt.replace(day=1)
    end_date = (start_date + datetime.timedelta(days=31)).replace(day=1)
    existing_timesheets = Timesheet.objects.filter(
        employee=employee,
        date__gte=start_date,
        date__lt=end_date,
    ).order_by("date")

    # Create timesheets for missing days in the month
    existing_dates = set(timesheet.date for timesheet in existing_timesheets)
    all_dates = set((start_date + datetime.timedelta(days=i)) for i in range((end_date - start_date).days))
    missing_dates = all_dates - existing_dates

    for missing_date in missing_dates:
        Timesheet.objects.create(employee=employee, date=missing_date, hours=0)

    return Timesheet.objects.filter(
        employee=employee,
        date__gte=start_date,
        date__lt=end_date,
    ).order_by("date")


@login_required
def index_view(request: HttpRequest):
    return redirect("cal:user", user_id=request.user.id)


@login_required
def cal_view(request: HttpRequest, user_id: int):
    employee = Employee.objects.get(id=user_id)
    current_date = datetime.date.today()

    timesheets = get_employee_timesheet_for_month(
        employee,
        current_date,
    )

    return render(
        request,
        "cal/index.html",
        {
            "timesheets": timesheets,
            "date": current_date,
        },
    )


@login_required
@csrf_exempt
def submit_timesheet_view(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        if not isinstance(data, dict):
            messages.error(request, "Invalid data format.")
            return redirect("cal:index")

        date = data.get("date")
        description = data.get("description")
        hours = data.get("hours")
        attachments = data.get("attachments")

        if not date or not description or not hours:
            return HttpResponse(
                json.dumps({"error": "All fields are required."}),
                content_type="application/json",
                status=400,
            )

        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            hours = float(hours)
        except ValueError:
            return HttpResponse(
                json.dumps({"error": "Invalid date or hours worked."}),
                content_type="application/json",
                status=400,
            )

        Timesheet.objects.create(
            employee=request.user,
            date=date,
            description=description,
            hours=hours,
            attachments=attachments,
        )

        return redirect("cal:index")

    return redirect("cal:index")


@login_required
def approve_timesheet_view(request: HttpRequest, timesheet_id: int):
    try:
        timesheet = Timesheet.objects.get(id=timesheet_id)
        if request.user == timesheet.employee.manager:
            timesheet.is_approved = True
            timesheet.save()
            messages.success(request, "Timesheet approved successfully.")
            return redirect("cal:user", user_id=timesheet.employee.id)
        else:
            messages.error(request, "You are not authorized to approve this timesheet.")
    except Timesheet.DoesNotExist:
        messages.error(request, "Timesheet does not exist.")

    return redirect("cal:index")


@login_required
@csrf_exempt
def upload_file_view(request: HttpRequest):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return HttpResponse(
                json.dumps({"error": "No file uploaded."}),
                content_type="application/json",
                status=400,
            )

        upload_path = os.path.join("uploads", file.name)
        with open(upload_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        if os.path.exists(upload_path):
            return HttpResponse(
                json.dumps({"message": "File uploaded successfully."}),
                content_type="application/json",
                status=200,
            )
        else:
            return HttpResponse(
                json.dumps({"error": "File upload failed."}),
                content_type="application/json",
                status=500,
            )

    return redirect("cal:index")


def get_uploads_view(request: HttpRequest, fname: str):
    return FileResponse(open(f"uploads/{fname}", "rb"))
