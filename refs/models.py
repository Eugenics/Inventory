from django.db import models
from django.urls import reverse, reverse_lazy
from decimal import Decimal
from django.contrib.auth.models import User

#from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget


class CustomBooleanField(models.BooleanField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        elif value == 0:
            return False
        else:
            return True

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        elif value == True:
            return 1
        else:
            return 0

    def get_db_prep_save(self, value, connection):
        return self.get_db_prep_value(value,
                                      connection=connection,
                                      prepared=False)


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True, verbose_name='Код')
    region_name = models.CharField(max_length=255,
                                   verbose_name='Наименование региона')
    objects = models.Manager()

    def __str__(self):
        return f'{self.region_name}'

    class Meta:
        db_table = '"inventory"."Region"'
        managed = False
        ordering = ['region_id']

    def get_absolute_url(self):
        return reverse('Region-detail', args=[str(self.region_id)])

    objects = models.Manager()


class House(models.Model):
    houses_id = models.AutoField(primary_key=True, verbose_name='Код')
    houses_name = models.CharField(max_length=255, verbose_name='Наименование')
    houses_rem = models.CharField(max_length=255,
                                  verbose_name='Примечание',
                                  blank=True)
    houses_region_id = models.ForeignKey(Region,
                                         on_delete=models.DO_NOTHING,
                                         db_column='houses_region_id',
                                         verbose_name='Регион')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Houses"'
        managed = False
        ordering = ['houses_id']

    def __str__(self):
        return f'{self.houses_region_id}' + ' | ' + f'{self.houses_name}'

    #def __str__(self):
    #    return f'{self.houses_name}'

    def get_absolute_url(self):
        return reverse('house_update', args=[str(self.houses_id)])

    def get_delete_url(self):
        return reverse('house_delete', args=[str(self.houses_id)])


class Office(models.Model):
    office_id = models.AutoField(primary_key=True, verbose_name='Код')
    office_name = models.CharField(max_length=255, verbose_name='Номер офиса')
    office_notes = models.CharField(max_length=255,
                                    null=True,
                                    blank=True,
                                    default="",
                                    verbose_name='Примечание')
    office_houses_id = models.ForeignKey(House,
                                         on_delete=models.DO_NOTHING,
                                         db_column='office_houses_id',
                                         verbose_name='Здание')
    office_is_store = CustomBooleanField(default=0, verbose_name='Склад')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Offices"'
        managed = False
        ordering = ['office_houses_id', 'office_name']

    #def __str__(self):
    #    return f'{self.office_houses_id}' + ' | ' + f'{self.office_name}'

    def __str__(self):
        return f'{self.office_name}'

    def get_absolute_url(self):
        return reverse('office_update', args=[str(self.office_id)])

    def get_delete_url(self):
        return reverse('office_delete', args=[str(self.office_id)])

    def get_is_store(self):
        if self.office_is_store == 0:
            return 'Нет'
        else:
            return 'Да'


class Department(models.Model):
    department_id = models.AutoField(primary_key=True, verbose_name='Код')
    department_name = models.CharField(max_length=255,
                                       verbose_name='Наименование',
                                       blank=True)
    department_notes = models.CharField(max_length=4000,
                                        verbose_name='Примечания',
                                        blank=True)
    department_region_id = models.ForeignKey(Region,
                                             on_delete=models.DO_NOTHING,
                                             db_column='department_region_id',
                                             verbose_name='Регион')
    department_parent_id = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        db_column='department_parent_id',
        verbose_name='Головное подразделение',
        blank=True)
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Departments"'
        managed = False
        ordering = ['department_region_id', 'department_id']

    #def __str__(self):
    #    return f'{self.department_region_id}' + ' | ' + f'{self.department_name}'

    def __str__(self):
        return f'{self.department_name}'

    def get_absolute_url(self):
        return reverse('department_update', args=[str(self.department_id)])

    def get_delete_url(self):
        return reverse('department_delete', args=[str(self.department_id)])

    def get_department_list(self):
        return reverse_lazy('department')


class Position(models.Model):
    position_id = models.AutoField(primary_key=True, verbose_name='Код')
    position_name = models.CharField(max_length=255, verbose_name='Должность')
    position_notes = models.CharField(max_length=255,
                                      verbose_name='Примечание',
                                      blank=True)
    position_department_id = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column='position_department_id',
        verbose_name='Подразделение')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Positions"'
        managed = False
        ordering = ['position_department_id', 'position_id']

    def __str__(self):
        return f'{self.position_department_id}' + ' | ' + f'{self.position_name}'

    def get_absolute_url(self):
        return reverse('position_update', args=[str(self.position_id)])

    def get_delete_url(self):
        return reverse('position_delete', args=[str(self.position_id)])

    def get_position_list(self):
        return reverse_lazy('position')


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, verbose_name='Код')
    employee_lastname = models.CharField(max_length=50,
                                         verbose_name='Фамилия',
                                         blank=True)
    employee_firstname = models.CharField(max_length=50,
                                          verbose_name='Имя',
                                          blank=True)
    employee_middlename = models.CharField(max_length=50,
                                           verbose_name='Отчество',
                                           blank=True)
    employee_email = models.CharField(max_length=150,
                                      verbose_name='email',
                                      blank=True)
    employee_position_id = models.ForeignKey(Position,
                                             on_delete=models.DO_NOTHING,
                                             db_column='employee_position_id',
                                             verbose_name='Должность')
    employee_office_id = models.ForeignKey(Office,
                                           on_delete=models.DO_NOTHING,
                                           db_column='employee_office_id',
                                           verbose_name='Офис')
    employee_phone_work = models.CharField(max_length=50,
                                           verbose_name='тел.',
                                           blank=True)
    employee_note = models.TextField(max_length=255,
                                     verbose_name='Примечание',
                                     blank=True)
    employee_full_fio = models.CharField(max_length=150,
                                         verbose_name='ФИО польностью',
                                         blank=True)
    employee_is_chief = CustomBooleanField(verbose_name='Руководитель',
                                           default=0)
    employee_is_respons = CustomBooleanField(verbose_name='Ответственный',
                                             default=0)
    user_id = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   db_column='user_id',
                                   verbose_name='Пользователь',
                                   blank=True)
    employee_is_mol = CustomBooleanField(verbose_name='МО', default=0)
    employee_region_id = models.ForeignKey(Region,
                                           on_delete=models.DO_NOTHING,
                                           db_column='employee_region_id',
                                           verbose_name='Регион')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Employees"'
        managed = False
        ordering = ['employee_id']

    def __str__(self):
        #return f'{self.employee_lastname}' + ' ' + f'{self.employee_firstname}' + ' ' + f'{self.employee_middlename}'
        return f'{self.employee_full_fio}'

    def get_absolute_url(self):
        return reverse('employee_update', args=[str(self.employee_id)])

    def get_delete_url(self):
        return reverse('employee_delete', args=[str(self.employee_id)])

    def get_employee_list(self):
        return reverse_lazy('employee')

    def get_is_respons_to_check(self):
        if self.employee_is_respons == 1:
            return 'checked'
        else:
            return ''

    def get_is_chief_to_check(self):
        if self.employee_is_chief == 1:
            return 'checked'
        else:
            return ''


class MCCat(models.Model):
    wcat_id = models.AutoField(primary_key=True, verbose_name='Код')
    wcatname = models.CharField(max_length=255, verbose_name='Наименование')
    wcatnotes = models.CharField(max_length=255,
                                 verbose_name='Примечание',
                                 blank=True)
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Wealth_Categories"'
        managed = False
        ordering = ['wcat_id']

    def __str__(self):
        return f'{self.wcatname}'


    def get_absolute_url(self):
        return reverse('mccat_update', args=[str(self.wcat_id)])

    def get_delete_url(self):
        return reverse('mccat_delete', args=[str(self.wcat_id)])

    def get_mccat_list(self):
        return reverse_lazy('mccat')


class MCType(models.Model):
    wtype_id = models.AutoField(primary_key=True, verbose_name='Код')
    wtype_name = models.CharField(max_length=255, verbose_name='Наименование')
    wtype_notes = models.CharField(max_length=255,
                                   verbose_name='Примечание',
                                   blank=True)
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Wealth_Types"'
        managed = False
        ordering = ['wtype_id']

    def __str__(self):
        return f'{self.wtype_name}'

    def get_absolute_url(self):
        return reverse('mctype_update', args=[str(self.wtype_id)])

    def get_delete_url(self):
        return reverse('mctype_delete', args=[str(self.wtype_id)])

    def get_mctype_list(self):
        return reverse_lazy('mctype')
