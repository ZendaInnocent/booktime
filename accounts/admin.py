from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.models import CustomUser, Address
from accounts.forms import UserChangeForm, UserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # The form to change user instances
    form = UserChangeForm

    # The form to create user instances
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal info',
            {'fields': ('name', )},
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    ordering = ('email', )
    filter_horizontal = ()
    search_fields = ('email', 'name', )
    list_filter = ('is_superuser', )
    list_display = ('email',
                    'name',
                    'is_staff', )


# admin.site.register(CustomUser, CustomUserAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'zip_code', 'city', 'country', )

    def name(self, obj):
        return obj.user.name


admin.site.register(Address, AddressAdmin)

admin.site.unregister(Group)
