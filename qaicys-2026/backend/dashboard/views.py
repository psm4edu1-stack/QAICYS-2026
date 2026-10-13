from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST


def manager_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard:index")

    form = AuthenticationForm(request, data=request.POST or None)
    access_error = ""
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.is_superuser:
            login(request, user)
            next_url = request.GET.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("dashboard:index")
        access_error = "This account does not have manager access."

    return render(request, "dashboard/login.html", {
        "form": form,
        "access_error": access_error,
        "frontend_url": settings.FRONTEND_URL,
    })


@require_http_methods(["GET"])
def index(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect_to_login(request.get_full_path())
    return render(request, "dashboard/index.html")


@require_POST
def manager_logout(request):
    logout(request)
    return redirect("dashboard:login")
