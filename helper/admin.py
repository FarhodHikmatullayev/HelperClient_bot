from django.contrib import admin
from .models import Users, Fikr, Filial, DepartmentFilial, Department, Promocode, Employee


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(DepartmentFilial)
class DepartmentFilialAdmin(admin.ModelAdmin):
    pass


@admin.register(Fikr)
class FikrAdmin(admin.ModelAdmin):
    pass


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    pass
