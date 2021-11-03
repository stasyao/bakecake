from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UsersCount


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phonenumber', 'address', 'social_network')}),
    )


@admin.register(UsersCount)
class UsersCountAdmin(admin.ModelAdmin):
    change_list_template = 'admin/users_count_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            users = response.context_data['cl'].queryset.filter(is_staff=False)
        except (AttributeError, KeyError):
            return response

        response.context_data['amount'] = len(users)

        return response


admin.site.register(CustomUser, CustomUserAdmin)
