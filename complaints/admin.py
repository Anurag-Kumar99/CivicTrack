from django.contrib import admin
from .models import User, Department, EmployeeProfile, Complaint
from  django.contrib.auth.admin import UserAdmin

# admin.site.register(User)
admin.site.register(Department)
admin.site.register(EmployeeProfile)
admin.site.register(Complaint)

@admin.register(User)
class customUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_active')