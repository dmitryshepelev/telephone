from django.contrib import admin
from telephone.main_app.models import UserProfile, Schema


class SchemaAdmin(admin.ModelAdmin):
	list_display = ('schema_code', 'name',)
	search_fields = ('schema_code', 'name',)


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'user_code', 'secret_key', 'schema',)
	raw_id_fields = ('schema', 'user',)


admin.site.register(Schema, SchemaAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
