from django.contrib import admin

from telephone.main_app.models import UserProfile, RedirectNumbers


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'profile_email', 'profile_password', 'uid', 'token', 'user_key', 'secret_key', 'profile_phone_number', 'date_subscribe_ended',)
	search_fields = ['profile_email', 'profile_phone_number']
	list_filter = ('date_subscribe_ended',)


class RedirectNumbersAdmin(admin.ModelAdmin):
	list_display = ('number', 'user_profile',)


admin.site.register(RedirectNumbers, RedirectNumbersAdmin)
admin.site.register(UserProfile, UserProfileAdmin)