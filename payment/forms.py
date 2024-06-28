from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ("S", "Stripe"),
    ("P", "PayPal"),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Street address",
                "class": "form-control",
            }
        )
    )
    apartment_address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apartment, suite, unit etc. (optional)",
                "class": "form-control",
            }
        ),
    )
    country = CountryField(blank_label="(select country)").formfield(
        required=False, widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Zip Code",
                "class": "form-control",
            }
        )
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )
