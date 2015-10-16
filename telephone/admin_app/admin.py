from django.contrib import admin
from telephone.main_app.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'profile_email', 'profile_password', 'uid', 'token', 'user_key', 'secret_key')


admin.site.register(UserProfile, UserProfileAdmin)
