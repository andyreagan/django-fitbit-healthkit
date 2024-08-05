# a simple view that just loads index.html
# and puts the user in the context
from datetime import date

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django_fitbit_healthkit.methods import (activity_intraday_by_date,
                                             daily_activity_summary,
                                             sleep_log_by_date)


def index(request: HttpRequest) -> HttpResponse:
    # if the user is logged in, get the daily fitbit data
    context = {"user": request.user}
    if request.user.is_authenticated and hasattr(request.user, "fitbituser"):
        context["daily_activity"] = daily_activity_summary(
            request.user.fitbituser, date.today()
        )
        context["sleep_log"] = sleep_log_by_date(request.user.fitbituser, date.today())
        context["activity_intraday"] = activity_intraday_by_date(
            request.user.fitbituser, "steps", date.today(), "15min"
        )
    return render(request, "sample/index.html", context)


def login_view(request):
    if request.method == "POST":
        print(request.POST)
        form = AuthenticationForm(request, data=request.POST)
        register_form = UserCreationForm(request.POST)
        if "login" in request.POST:
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect("home")
            else:
                # return to the login page with the errors
                return render(
                    request, "sample/login.html", {"form": form, "errors": form.errors}
                )
        elif "register" in request.POST:
            if register_form.is_valid():
                user = register_form.save()
                auth_login(request, user)
                return redirect("home")
            else:
                # return to the registration page with the errors
                return render(request, "sample/register.html", {"form": register_form})
    else:
        form = AuthenticationForm()
        register_form = UserCreationForm()
    return render(request, "sample/login.html", {"form": form})


def logout_view(request):
    """Log out the user"""
    logout(request)
    return redirect("home")


def register_view(request):
    form = UserCreationForm()
    return render(request, "sample/register.html", {"form": form})
