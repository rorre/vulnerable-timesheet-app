from django.shortcuts import redirect, render
from django.contrib import messages

from authentication.models import Employee
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index_view(request):
    if getattr(request.user, "is_admin", False):
        messages.info(request, "You are not allowed to access this page.")
        return redirect("index")

    users = Employee.objects.all()
    return render(request, "administrator/index.html", {"users": users})


@login_required
def set_manager_view(request, user_id):
    if request.method == "POST":
        maneger_id = request.POST.get("manager_id")

        if not maneger_id:
            messages.error(request, "Manager ID are required.")
            return redirect("administrator:index")

        try:
            user = Employee.objects.get(id=user_id)
            manager = Employee.objects.get(id=maneger_id)
            user.manager = manager
            user.save()
            messages.success(request, "Manager set successfully.")
        except Exception as e:
            messages.error(request, "User or Manager does not exist.")

    return redirect("administrator:index")
