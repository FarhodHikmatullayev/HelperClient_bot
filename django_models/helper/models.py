from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'users'


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'filial'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'department'


class DepartmentFilial(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    filial = models.ForeignKey('Filial', on_delete=models.CASCADE)

    class Meta:
        db_table = 'department_filial'


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    filial = models.ForeignKey('Filial', on_delete=models.CASCADE)
    code = models.CharField(max_length=3, null=False)

    class Meta:
        db_table = 'employee'


# class Fikr(models.Model):
#     id = models.AutoField(primary_key=True)
#     message = models.TextField(null=True)
#     user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
#     mark = models.IntegerField(null=True, validators=[
#         MinValueValidator(1),
#         MaxValueValidator(5),
#     ])
#     department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)
#     employee_code = models.IntegerField(null=True)
#     branch = models.ForeignKey('Filial', on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(default=timezone.now, null=True)
#
#     class Meta:
#         db_table = 'fikr'


class Fikr(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField(null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    mark = models.IntegerField(null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)
    employee_code = models.IntegerField(null=True)
    branch = models.ForeignKey('Filial', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now(), null=True)

    class Meta:
        db_table = 'fikr'
        constraints = [
            models.CheckConstraint(check=models.Q(mark__gte=1) & models.Q(mark__lte=5), name='fikr_mark_check'),
        ]


class Promocode(models.Model):
    id = models.AutoField(primary_key=True)
    promocode = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table = 'promocodes'
