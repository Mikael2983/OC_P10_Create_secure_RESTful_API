from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # Show custom fields in the user list
    list_display = (
        'id', 'username', 'email', 'birth_date', 'can_be_contacted',
        'can_data_be_shared', 'is_staff')

    # Adding custom fields in the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires',
         {'fields': ('birth_date', 'can_be_contacted', 'can_data_be_shared')}),
    )

    # Adding custom fields in the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires',
         {'fields': ('birth_date', 'can_be_contacted', 'can_data_be_shared')}),
    )


admin.site.register(User, CustomUserAdmin)
