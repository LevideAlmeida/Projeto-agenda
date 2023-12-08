from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms
from . import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "accept": "image/*"
            }
        ),
        required=False
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


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text="Required.",
        error_messages={
            "min_length": "Please, add more than 2 letters",
            "max_length": "Please, add less than 30 letters",
            },
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text="Required.",
        error_messages={
            "min_length": "Please, add more than 2 letters",
            "max_length": "Please, add less than 30 letters",
            },
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "username",
                  )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    ValidationError("The passwords are not equals")
                    )
                print(password1, password2)

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        "Já existe um usuario com este e-mail", code="invalid"
                    )
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password1', ValidationError(errors))

        return password1
