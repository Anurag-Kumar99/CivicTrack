from django.contrib import admin
from .models import User, Department, EmployeeProfile, Complaint
from  django.contrib.auth.admin import UserAdmin

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'priority', 'status', 'assigned_employee')
    list_filter = ('department', 'priority', 'status')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'role', 'department', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {
            'fields': ('role', 'department'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'department', 'password1', 'password2'),
        }),
    )
