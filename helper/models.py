from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name="USERNAME")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="TELEFON RAQAM")
    telegram_id = models.BigIntegerField(unique=True, verbose_name="TELEGRAM ID")
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="F.I.SH")

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.full_name


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="NOMI")

    class Meta:
        db_table = 'filial'
        verbose_name = "Branch"
        verbose_name_plural = "Filiallar"

    def __str__(self):
        return self.name


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="NOMI")

    class Meta:
        db_table = 'department'
        verbose_name = "Rank"
        verbose_name_plural = "Lavozimlar"

    def __str__(self):
        return self.name


class DepartmentFilial(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="LAVOZIM")
    filial = models.ForeignKey('Filial', on_delete=models.CASCADE, verbose_name="FILIAL")

    class Meta:
        db_table = 'department_filial'
        verbose_name = "RankFilial"
        verbose_name_plural = "Filial-Lavozim"

    def __str__(self):
        return f"{self.filial.name} - {self.department.name}"


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=False, verbose_name="F.I.SH")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="LAVOZIM")
    filial = models.ForeignKey('Filial', on_delete=models.CASCADE, verbose_name="FILIAL")
    code = models.CharField(max_length=3, null=False, verbose_name="MAXSUS KOD")

    class Meta:
        db_table = 'employee'
        verbose_name = "Employee"
        verbose_name_plural = "Xodimlar"

    def __str__(self):
        return self.full_name


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
    message = models.TextField(null=True, verbose_name="IZOH")
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, verbose_name="BAHOLAGAN SHAXS")
    mark = models.IntegerField(null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], verbose_name="BAHO")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, verbose_name="LAVOZIM",
                                   blank=True)
    employee_code = models.IntegerField(null=True, verbose_name="XODIM KODI")
    branch = models.ForeignKey('Filial', on_delete=models.CASCADE, null=True, verbose_name="FILIAL")
    created_at = models.DateTimeField(default=timezone.now, null=True, verbose_name="BAHOLANGAN VAQT")

    class Meta:
        db_table = 'fikr'
        constraints = [
            models.CheckConstraint(check=models.Q(mark__gte=1) & models.Q(mark__lte=5), name='fikr_mark_check'),
        ]
        verbose_name = "Comment"
        verbose_name_plural = "Bildirilgan fikrlar"

    def __str__(self):
        return f"{self.user.full_name} ning {self.branch.name} filiali {self.employee_code} ID raqamli xodimga bildirgan fikri"


class Promocode(models.Model):
    id = models.AutoField(primary_key=True)
    promocode = models.CharField(max_length=50, unique=True, verbose_name="PROMO KOD")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, verbose_name="PROMO KOD EGASI")
    created_at = models.DateTimeField(default=timezone.now, null=True, verbose_name="YARATILGAN VAQT")

    class Meta:
        db_table = 'promocodes'
        verbose_name = "Promo code"
        verbose_name_plural = "Promo kodlar"

    def __str__(self):
        return f"{self.user.full_name} ning {self.promocode} raqamli promocodi"
