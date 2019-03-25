from django.db import models
from django.urls import reverse, reverse_lazy
from decimal import Decimal
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget


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

    def get_db_prep_save(self,value,connection):
        return self.get_db_prep_value(value, connection=connection,prepared=False)


# Create your models here.

class Region(models.Model):
    region_id = models.IntegerField(primary_key=True,verbose_name='Код')
    region_name = models.CharField(max_length=255,verbose_name='Наименование региона')
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
    houses_id = models.AutoField(primary_key=True,verbose_name='Код')
    houses_name = models.CharField(max_length=255,verbose_name='Наименование')
    houses_rem = models.CharField(max_length=255,verbose_name='Примечание')
    houses_region_id = models.ForeignKey(Region,on_delete=models.DO_NOTHING,db_column='houses_region_id',verbose_name='Регион')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Houses"'
        managed = False
        ordering = ['houses_id']
    
    def __str__(self):       
        return f'{self.houses_region_id}' + ' | ' + f'{self.houses_name}'
    
    def get_absolute_url(self):        
        return reverse('house_update', args=[str(self.houses_id)])
    
    def get_delete_url(self):
        return reverse('house_delete',args=[str(self.houses_id)])
    

class Office(models.Model):
    office_id  = models.AutoField(primary_key=True,verbose_name='Код')
    office_name = models.CharField(max_length=255,verbose_name='Номер офиса')
    office_notes = models.CharField(max_length=255,null=True,blank=True,default="",verbose_name='Примечание')
    office_houses_id = models.ForeignKey(House,on_delete=models.DO_NOTHING,db_column='office_houses_id',verbose_name='Здание')
    office_is_store = CustomBooleanField(default=0,verbose_name='Склад')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Offices"'
        managed = False
    
    def __str__(self):
        return f'{self.office_houses_id}' + ' | ' + f'{self.office_name}'

    def get_absolute_url(self):
        return reverse('office_update',args=[str(self.office_id)])
    
    def get_delete_url(self):
        return reverse('office_delete',args=[str(self.office_id)])
    
    def get_is_store(self):
        if self.office_is_store == 0:
            return 'Нет'
        else:
            return 'Да'

    
class Department(models.Model):
    department_id = models.AutoField(primary_key=True,verbose_name='Код')
    department_name = models.CharField(max_length=255,verbose_name='Наименование')
    department_notes = models.CharField(max_length=4000,verbose_name='Примечания',null=True)
    department_region_id = models.ForeignKey(Region,on_delete=models.DO_NOTHING,db_column='department_region_id',verbose_name='Регион')
    department_parent_id = models.ForeignKey("self",on_delete=models.DO_NOTHING,db_column='department_parent_id',verbose_name='Головное подразделение')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Departments"'
        managed = False
        ordering = ['department_region_id','department_id']
    
    def __str__(self):       
        return f'{self.department_region_id}' + ' | ' + f'{self.department_name}'
    
    def get_absolute_url(self):        
        return reverse('department_update', args=[str(self.department_id)])
    
    def get_delete_url(self):
        return reverse('department_delete',args=[str(self.department_id)])
    
    def get_department_list(self):
        return reverse_lazy('department')

class Position(models.Model):
    position_id = models.AutoField(primary_key=True,verbose_name='Код')
    position_name = models.CharField(max_length=255,verbose_name='Должность')
    position_notes = models.CharField(max_length=255,verbose_name='Примечание')
    position_department_id = models.ForeignKey(Department,on_delete=models.DO_NOTHING,
        db_column='position_department_id',verbose_name='Подразделение')
    objects = models.Manager()
    
    class Meta:
        db_table = '"inventory"."Positions"'
        managed = False
        ordering = ['position_department_id','position_id']
    
    def __str__(self):       
        return f'{self.position_department_id}' + ' | ' + f'{self.position_name}'
    
    def get_absolute_url(self):        
        return reverse('position_update', args=[str(self.position_id)])
    
    def get_delete_url(self):
        return reverse('position_delete',args=[str(self.position_id)])
    
    def get_position_list(self):
        return reverse_lazy('position')


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True,verbose_name='Код')
    employee_lastname = models.CharField(max_length=255,verbose_name='Фамилия')
    employee_firstname = models.CharField(max_length=255,verbose_name='Имя')    
    employee_middlename = models.CharField(max_length=255,verbose_name='Отчество')
    employee_email = models.CharField(max_length=255,verbose_name='email',blank=True,null=True)
    employee_position_id = models.ForeignKey(Position,on_delete=models.DO_NOTHING,db_column='employee_position_id',verbose_name='Должность')
    employee_office_id = models.ForeignKey(Office,on_delete=models.DO_NOTHING,db_column='employee_office_id',verbose_name='Офис')
    employee_phone_work = models.CharField(max_length=255,verbose_name='тел.',blank=True,default='')
    employee_note = models.CharField(max_length=255,verbose_name='Примечание',blank=True)
    employee_full_fio = models.CharField(max_length=255,verbose_name='ФИО польностью')
    employee_is_chief = CustomBooleanField(verbose_name='Руководитель',default=0)
    employee_is_respons = CustomBooleanField(verbose_name='МО лицо',default=0)
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Employees"'
        managed = False
        ordering = ['employee_id']
    
    def __str__(self):       
        return f'{self.employee_lastname}' + ' ' + f'{self.employee_firstname}' + ' ' + f'{self.employee_middlename}'
    
    def get_absolute_url(self):        
        return reverse('employee_update', args=[str(self.employee_id)])
    
    def get_delete_url(self):
        return reverse('employee_delete',args=[str(self.employee_id)])
    
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
    wcat_id = models.AutoField(primary_key=True,verbose_name='Код')
    wcatname = models.CharField(max_length=255,verbose_name='Наименование')
    wcatnotes = models.CharField(max_length=255,verbose_name='Примечание',blank=True)
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Wealth_Categories"'
        managed = False
        ordering = ['wcat_id']
    
    def __str__(self):       
        return f'{self.wcatname}'

class MCType(models.Model):
    wtype_id = models.AutoField(primary_key=True,verbose_name='Код')
    wtype_name = models.CharField(max_length=255,verbose_name='Наименование')
    wtype_notes = models.CharField(max_length=255,verbose_name='Примечание',blank=True)
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
        return reverse('mctype_delete',args=[str(self.wtype_id)])
    
    def get_mctype_list(self):
        return reverse_lazy('mctype')

class Hardware(models.Model):
    whard_id =  models.AutoField(primary_key=True,verbose_name='Код')
    whard_inumber = models.CharField(max_length=30,verbose_name='Инв. номер')
    whard_fnumber = models.CharField(max_length=65,verbose_name='Заводской номер')
    whard_wcat_id = models.ForeignKey(MCCat,on_delete=models.DO_NOTHING,
        db_column ='whard_wcat_id',verbose_name='Категория')
    whard_wtype_id = models.ForeignKey(MCType,on_delete=models.DO_NOTHING,
        db_column ='whard_wtype_id',verbose_name='Тип')
    whard_name = models.CharField(max_length=255,verbose_name='Наименование')
    whard_date_of_adoption = models.DateField(verbose_name='Дата постановки на учет')
    whard_initial_cost = models.DecimalField(verbose_name='Начальная стоимость',blank=True,
        max_digits=18,decimal_places=2,default=Decimal('0.00'))
    whard_residual_value = models.DecimalField(verbose_name='Остаточная стоимость',blank=True,
        max_digits=18,decimal_places=2,default=Decimal('0.00'))
    whard_office_id = models.ForeignKey(Office,on_delete=models.DO_NOTHING,db_column='whard_office_id',verbose_name='Офис')
    whard_note = models.CharField(max_length=65,verbose_name='Примечание',blank=True)
    whard_archiv = CustomBooleanField (verbose_name='Архив')
    objects = models.Manager()

    class Meta:
        db_table = '"inventory"."Wealth_Hardware"'
        managed = False
        ordering = ['whard_id']
    
    def __str__(self):       
        return f'{self.whard_name}'
    
    def get_absolute_url(self):        
        return reverse('hardware_update', args=[str(self.whard_id)])
    
    def get_delete_url(self):
        return reverse('hardware_delete',args=[str(self.whard_id)])
    
    def get_hardware_list(self):
        return reverse_lazy('hardware')

class RelOfficeResp (models.Model):
    roe_id = models.AutoField(primary_key=True,verbose_name='Код')
    roe_office_id = models.ForeignKey(Office,on_delete=models.DO_NOTHING,db_column='roe_office_id',verbose_name='Офис')
    roe_employee_id = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,db_column='roe_employee_id',verbose_name='Сотрудник')
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
        return reverse('relofficeresp_delete',args=[str(self.roe_id)])
    
    def get_relofficeresp_list(self):
        return reverse_lazy('relofficeresp')