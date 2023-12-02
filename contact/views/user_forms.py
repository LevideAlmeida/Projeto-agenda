from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from contact.forms import RegisterForm


def register(request):
    form = RegisterForm()

    # messages.info(request, "info")
    # messages.warning(request, "warning")
    # messages.success(request, "success")
    # messages.error(request, "error")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario salvo")
            return redirect("contact:login")

    context = {
        "site_title": "Create - User",
        "form": form,
    }
    return render(request, "contact/register.html", context)


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Login efetuado com sucesso")
            return redirect("contact:index")

    context = {
        "site_title": "LOGIN",
        "form": form,
    }
    return render(request, "contact/login.html", context)


def logout_view(request):
    auth.logout(request)
    return redirect("contact:login")
