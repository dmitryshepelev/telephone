from django import forms


class AuthUserForm(forms.Form):
	"""
	Represents model from login form
	"""
	username = forms.CharField(min_length=3, max_length=15)
	password = forms.CharField(min_length=6)


class ProfileRequestForm(forms.Form):
	"""
	Represents model from login form
	"""
	email = forms.EmailField(min_length=5)
