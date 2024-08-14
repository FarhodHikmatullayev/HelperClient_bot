from django.contrib import admin
from .models import Users, Fikr, Filial, DepartmentFilial, Department, Promocode, Employee


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'telegram_id', 'full_name')
    search_fields = ('username', 'phone', 'telegram_id', 'full_name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'department__name', 'filial__name', 'code')
    search_fields = ('full_name', 'department__name', 'filial__name', 'code')


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(DepartmentFilial)
class DepartmentFilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'filial__name', 'department__name')
    search_fields = ('filial__name', 'department_name')


@admin.register(Fikr)
class FikrAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user__full_name', 'user__phone', 'department__name', 'branch__name', 'employee_code',
        'created_at')
    search_fields = (
        'employee_code', 'user__full_name', 'user__phone', 'department__name', 'branch__name', 'employee_code')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'promocode', 'user__username', 'user__phone', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('promocode', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('promocode', 'user_username', 'user__phone')
