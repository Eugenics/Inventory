from django.contrib import admin
from refs.models import House, Region, Office, Department, Position, Employee, MCCat, MCType
from catalog.models import RelHardEmp, RelOfficeResp, Hardware

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Permission


#class EmployeeInline(admin.StackedInline):
#    model = Employee
#    can_delete = False
#    verbose_name_plural = 'Сотрудник'


# Define a new User admin
#class UserAdmin(BaseUserAdmin):
#    inlines = (EmployeeInline, )


# Register your models here.
admin.site.register(House)
admin.site.register(Region)
admin.site.register(Office)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(MCCat)
admin.site.register(MCType)
admin.site.register(Hardware)
admin.site.register(RelOfficeResp)
admin.site.register(RelHardEmp)

# Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

admin.site.register(Permission)
