from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

from courses.models import Course

User = get_user_model()

PAYMENT_CHOICES = (
    ("S", "Stripe"),
    ("P", "PayPal"),
)

ADDRESS_CHOICES = (
    ("B", "Billing"),
    ("S", "Shipping"),
)


class OrderCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.course.price}"

    def get_total_items_price(self):
        return self.quantity * self.course.price

    def get_final_price(self):
        return self.get_total_items_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderCourse)
    ordered = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=1, choices=PAYMENT_CHOICES)
    payment = models.ForeignKey(
        "Payment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="billing_address",
    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"


class Payment(models.Model):
    charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    payment_option = models.CharField(max_length=1, choices=PAYMENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
