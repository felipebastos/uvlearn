# uvauth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Informações pessoais'),
            {'fields': ('first_name', 'last_name', 'campus', 'vinculo')},
        ),
        (
            _('Permissões'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'vinculo', 'password1', 'password2'),
            },
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'campus', 'vinculo', 'is_staff')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'campus',
        'vinculo',
        'groups',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
