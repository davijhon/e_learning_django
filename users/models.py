from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ("S", "Stripe"),
    ("P", "PayPal"),
)


class CustomUser(AbstractUser):
    #: First and last name do not cover name patterns around the globe
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
                str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_address2 = models.CharField(max_length=255, blank=True, null=True)
    billing_country = CountryField(multiple=False, blank=True, null=True)
    billing_zip = models.CharField(max_length=255, blank=True, null=True)

    payment_option = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + " " + self.user.last_name
