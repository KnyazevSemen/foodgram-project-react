from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_active'
    )
    fields = (
        ('username', 'email', ),
        ('first_name', 'last_name', ),
        ('is_active', ),
    )
    fieldsets = []
    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'is_active', 'first_name', 'email',
    )
