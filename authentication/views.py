from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from authentication.models import Employee
from django.contrib import messages


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("cal:index")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("cal:index")
        else:
            error_message = "Invalid username or password."
            return render(request, "auth/login.html", {"error_message": error_message})
    return render(request, "auth/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("cal:index")
    
    if request.method == "POST":
        data = request.POST.dict()
        if data.get("password") != data.get("confirm_password"):
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/register.html")

        del data["confirm_password"]
        del data["csrfmiddlewaretoken"]
        try:
            user = Employee.objects.create_user(**data)
            user.save()
        except Exception as e:
            messages.error(request, "User already exists.")
            return render(request, "auth/register.html")
        return redirect("authentication:login")

    return render(request, "auth/register.html", {"error_message": None})


def logout_view(request):
    logout(request)
    return redirect("authentication:login")
