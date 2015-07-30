from django import forms


class AuthUserForm(forms.Form):
	username = forms.CharField(min_length=3, max_length=15)
	password = forms.CharField(min_length=6)

	@staticmethod
	def get_form_name():
		return 'auth_user_form'