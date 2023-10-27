from django.shortcuts import render, redirect
from contact.forms import ContactForm


def create(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        context = {
            'site_title': 'Contact - Create',
            'form': form,
        }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect("contact:create")

        return render(
            request,
            "contact/create.html",
            context,
        )

    context = {
        'site_title': 'Contact - Create',
        'form': ContactForm(),
    }

    return render(
        request,
        "contact/create.html",
        context,
    )
