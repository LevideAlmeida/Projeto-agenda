from django.core.exceptions import ValidationError
from django import forms
from . import models


class ContactForm(forms.ModelForm):
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

    class Meta:
        model = models.Contact
        fields = ("first_name", "last_name", "phone", "email")

        # Doc widget: https://docs.djangoproject.com/en/4.2/ref/forms/widgets/
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': "Insert E-mail here"
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

        self.add_error(
            "first_name",
            ValidationError(
                "Mensagem de erro",
                code="invalid",
            )
        )

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        print("passei no clean do first name")
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
