from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'date_of_birth', 'citizenship_number', 'country', 'province', 'city', 'zip_code')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )

    list_display = ['id', 'email', 'username', 'phone_number', 'is_active', 'is_superuser']
    search_fields = ['email', 'username']
    ordering = ['email', 'username']
    filter_horizontal = []

    # Added to ensure email is used for login in admin
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


# Register the User model with UserAdmin
admin.site.register(User, UserAdmin)