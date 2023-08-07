"""
Djanfo Admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # Customize the fieldsets class var and only specifies fields that
    # exist in our model
    fieldsets = (
        (None, {'fields': ['email', 'name']}),
        (
            # Use the '_' from the translation lib
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    # Prevent modifying the last_login filed
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            # 'classes' enables custom css
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )



#Specify UserAdmin to apply ordering and list display changes
admin.site.register(models.User, UserAdmin)
