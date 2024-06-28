from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm


CustomUser = get_user_model()


@admin.register(CustomUser)
class UserAdmin(auth_admin.UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    # fieldsets = (("User", {"fields": ("name", "stripe_customer_id")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser"]
    search_fields = ["name"]


