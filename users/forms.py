from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError 
from django import forms as normal_forms



User = get_user_model()



class CancelSubscriptionForm(normal_forms.Form):
	hidden = normal_forms.HiddenInput()


class CustomUserCreationForm(forms.UserCreationForm):

	error_message = forms.UserCreationForm.error_messages.update(
		{"duplicate_username": ("This username has already been taken.")}
	)

	class Meta(forms.UserCreationForm.Meta):
		model = User

	def clean_username(self):
		username = self.cleaned_data["username"]

		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username

		raise ValidationError(self.error_messages["duplicate_username"])


class CustomUserChangeForm(forms.UserChangeForm):

	class Meta(forms.UserChangeForm.Meta):
		model = User
		fields = ('email', 'first_name', 'last_name', 'photo',)