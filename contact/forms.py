from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*"
            }
        ),
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': "Insert first name here"
            }
        ),
        # label="LABEL",
        help_text="Texto de ajuda",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': "Insert last name here"
            }
        )

        self.fields['description'].widget.attrs.update(
            {
                'placeholder': "Description"
            }
        )

    class Meta:
        model = models.Contact
        fields = ("first_name", "last_name", "phone",
                  "email", "description", "category",
                  "picture",
                  )

        # Doc widget: https://docs.djangoproject.com/en/4.2/ref/forms/widgets/
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': "Insert E-mail here"
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': "Phone Number"
                }
            ),
        }

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        if first_name == last_name:
            msg = ValidationError(
                "First name and last name cannot be the same",
                code="invalid",
            )

            self.add_error("first_name", msg)
            self.add_error("last_name", msg)

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name == "ABC":
            self.add_error(
                "first_name",
                ValidationError(
                    "VEIO DO ADD_ERROR",
                    code="invalid",
                )
            )
        # raise ValidationError("Não digite ABC nesse campo", code="invalid")

        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
    )

    email = forms.EmailInput()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "username", "password1", "password2",
                  )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    "Já existe um usuario com este e-mail", code="invalid"
                )
            )

        return email
