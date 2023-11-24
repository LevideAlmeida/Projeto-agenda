from django.shortcuts import render, redirect
from django.contrib import messages
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
            return redirect("contact:index")

    context = {
        "site_title": "Create - User",
        "form": form,
    }
    return render(request, "contact/register.html", context)
