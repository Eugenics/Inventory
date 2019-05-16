from django.db import models
from django.urls import reverse, reverse_lazy
from decimal import Decimal
from refs.models import *
#from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
from django.contrib.auth.models import User


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


class Hardware(models.Model):
    whard_id = models.AutoField(primary_key=True, verbose_name='Код')
    whard_inumber = models.CharField(max_length=30, verbose_name='Инв. номер')
    whard_fnumber = models.CharField(max_length=65,
                                     verbose_name='Заводской номер',
                                     blank=True)
    whard_wcat_id = models.ForeignKey(MCCat,
                                      on_delete=models.DO_NOTHING,
                                      db_column='whard_wcat_id',
                                      verbose_name='Категория')
    whard_wtype_id = models.ForeignKey(MCType,
                                       on_delete=models.DO_NOTHING,
                                       db_column='whard_wtype_id',
                                       verbose_name='Тип')
    whard_name = models.CharField(max_length=255, verbose_name='Наименование')
    whard_date_of_adoption = models.DateField(
        verbose_name='Дата постановки на учет', blank=True)
    whard_initial_cost = models.DecimalField(
        verbose_name='Начальная стоимость',
        blank=True,
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'))
    whard_residual_value = models.DecimalField(
        verbose_name='Остаточная стоимость',
        blank=True,
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'))
    whard_office_id = models.ForeignKey(Office,
                                        on_delete=models.DO_NOTHING,
                                        db_column='whard_office_id',
                                        verbose_name='Офис')
    whard_note = models.CharField(max_length=65,
                                  verbose_name='Примечание',
                                  blank=True)
    whard_archiv = CustomBooleanField(verbose_name='Архив')
    whard_mol_employee_id = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        db_column='whard_mol_employee_id',
        verbose_name='МО')
    whard_region_id = models.ForeignKey(Region,
                                        on_delete=models.DO_NOTHING,
                                        db_column='whard_region_id',
                                        verbose_name='Регион')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Wealth_Hardware"'
        managed = False
        #ordering = ['whard_id']

    def __str__(self):
        return f'{self.whard_name}'

    def get_absolute_url(self):
        return reverse('hardware_update', args=[str(self.whard_id)])

    def get_delete_url(self):
        return reverse('hardware_delete', args=[str(self.whard_id)])

    def get_hardware_list(self):
        return reverse_lazy('hardware')


class RelOfficeResp(models.Model):
    roe_id = models.AutoField(primary_key=True, verbose_name='Код')
    roe_office_id = models.ForeignKey(Office,
                                      on_delete=models.DO_NOTHING,
                                      db_column='roe_office_id',
                                      verbose_name='Офис')
    roe_employee_id = models.ForeignKey(Employee,
                                        on_delete=models.DO_NOTHING,
                                        db_column='roe_employee_id',
                                        verbose_name='Сотрудник')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Rel_Office_Respons_Employee"'
        managed = False
        ordering = ['roe_id']

    def get_absolute_url(self):
        return reverse('relofficeresp_update', args=[str(self.roe_id)])

    def __str__(self):
        return f'{self.roe_employee_id}'

    def get_delete_url(self):
        return reverse('relofficeresp_delete', args=[str(self.roe_id)])

    def get_relofficeresp_list(self):
        return reverse_lazy('relofficeresp')


class RelHardEmp(models.Model):
    relhe_id = models.AutoField(primary_key=True, verbose_name='Код')
    relhe_employee_id = models.ForeignKey(Employee,
                                          on_delete=models.DO_NOTHING,
                                          db_column='relhe_employee_id',
                                          verbose_name='Сотрудник')
    relhe_whard_id = models.ForeignKey(Hardware,
                                       on_delete=models.DO_NOTHING,
                                       db_column='relhe_whard_id',
                                       verbose_name='Оборудование')

    class Meta:
        db_table = '"inventory"."Rel_Hardware_Employee"'
        managed = False
        ordering = ['relhe_id']

    #def get_absolute_url(self):
    #   return reverse('relhardemp_update', args=[str(self.relhe_id)])

    def __str__(self):
        return f'{self.relhe_employee_id}'

    #def get_delete_url(self):
    #    return reverse('relhardemp_delete', args=[str(self.relhe_id),f'{self.relhe_employee_id}'])
