from django.contrib import admin

from telephone.my_app.models import YandexProfile, PBX


class ModelAdminBase(admin.ModelAdmin):
	exclude = ('guid', 'creation_datetime', 'last_edited_datetime', 'exist')


class YandexProfileAdmin(ModelAdminBase):
	list_display = (
		'user',
		'yandex_email',
		'yandex_password',
		'uid',
		'token',
		'creation_datetime',
		'last_edited_datetime'
	)


class PBXAdmin(ModelAdminBase):
	list_display = (
		'user',
		'user_key',
		'secret_key',
		'phone_number',
		'customer_number',
		'sip',
		'creation_datetime',
		'last_edited_datetime'
	)


admin.site.register(YandexProfile, YandexProfileAdmin)
admin.site.register(PBX, PBXAdmin)
