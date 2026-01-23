from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'id',
        'user_id',
        'username',
        'phone',
        'is_active',
        'is_staff',
    )

    list_filter = ('is_active', 'is_staff')

    search_fields = ('username', 'phone')

    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('username', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
