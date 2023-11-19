from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from contact.models import Contact
from contact.forms import ContactForm


def create(request):
    form_action = reverse("contact:create")
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        context = {
            'site_title': 'Contact - Create',
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect("contact:update", contact_id=contact.pk)

        return render(
            request,
            "contact/create.html",
            context,
        )

    context = {
        'site_title': 'Contact - Create',
        'form': ContactForm(),
        'form_action': form_action,

    }

    return render(
        request,
        "contact/create.html",
        context,
    )


def update(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse("contact:update", args=(contact_id,))

    if request.method == "POST":
        form = ContactForm(data=request.POST, instance=contact)
        context = {
            'site_title': 'Contact - Update',
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect("contact:update", contact_id=contact.pk)

        return render(
            request,
            "contact/create.html",
            context,
        )

    context = {
        'site_title': 'Contact - Update',
        'form': ContactForm(instance=contact),
        'form_action': form_action,

    }

    return render(
        request,
        "contact/create.html",
        context,
    )
