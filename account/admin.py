from django.contrib import admin
from .models import CustomUser, LoggedIn, Pos
from ims.forms import UserCreateForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomStaffAdmin(UserAdmin):
    model = CustomUser
    add_form: UserCreateForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields': (
                    'pos',
                    'is_admin',
                    'is_sub_admin',
                    'is_work_staff',
                    'phone_number',
                    'address',
                    'is_subscribed'
                ),
            }

        )
    )

admin.site.register(CustomUser, CustomStaffAdmin)
admin.site.register(LoggedIn)
admin.site.register(Pos)
