from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'first_name', 'is_active', 'is_staff', 'is_superuser']
