from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'organization',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'organization',)


class CustomAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    ordering = ('email',)
    list_display = ('email', 'organization', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'organization')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'organization', 'password', 'date_joined', 'last_login')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'organization',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )}
         ),
    )

    filter_horizontal = ()
    list_filter = ()


admin.site.register(CustomUser, CustomAdmin)
