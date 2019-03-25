from django.shortcuts import render
from catalog.models import House, Office, Department, Position, Employee, MCCat, MCType, Region, Hardware,RelOfficeResp
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django import template

from .forms import HardwareForm,RelOfficeRespForm

register = template.Library()


@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_houses = House.objects.all().count()
    num_offices = Office.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_houses': num_houses,
        'num_offices': num_offices,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
#######################################################################################


#DASHBOARD
@login_required
def dashboard(request):
    num_houses = House.objects.all().count()
    num_offices = Office.objects.all().count()
    num_employees = Employee.objects.all().count()
    num_positions = Position.objects.all().count()
    num_departments = Department.objects.all().count()
    num_regions = Region.objects.all().count()
    num_mctype = MCType.objects.all().count()
    num_departments = Department.objects.all().count()

    context = {
        'num_houses': num_houses,
        'num_offices': num_offices,
        'num_employees': num_employees,
        'num_positions': num_positions,
        'num_departments': num_departments,
        'num_regions': num_regions,
        'num_mctype': num_mctype,
        'num_departments': num_departments,
    }
    return render(request, 'dashboard.html', context=context)
#######################################################################################


# HOUSE Class
class HouseListView(PermissionRequiredMixin, generic.ListView):
    model = House
    fields = '__all__'
    permission_required = 'catalog.view_house'
    #LoginRequiredMixin
    paginate_by = 10


class HouseDetailView(LoginRequiredMixin, generic.DetailView):
    model = House


class HouseCreate(PermissionRequiredMixin, CreateView):
    model = House
    fields = '__all__'
    permission_required = 'catalog.add_house'
    success_url = reverse_lazy('house')


class HouseUpdate(PermissionRequiredMixin, UpdateView):
    model = House
    fields = ['houses_name', 'houses_rem', 'houses_region_id']
    permission_required = 'catalog.change_house'
    success_url = reverse_lazy('house')


class HouseDelete(PermissionRequiredMixin, DeleteView):
    model = House
    success_url = reverse_lazy('house')
    permission_required = 'catalog.delete_house'
#######################################################################################

# OFFICE Class
class OfficeListView(PermissionRequiredMixin, generic.ListView):
    model = Office
    fields = '__all__'
    permission_required = 'catalog.view_office'
    #LoginRequiredMixin
    paginate_by = 10

    @property
    def get_total_list_count(self):
        return model.Office.objects.all().count()


class OfficeCreate(PermissionRequiredMixin, CreateView):
    model = Office
    fields = '__all__'
    permission_required = 'catalog.add_office'
    success_url = reverse_lazy('office')


class OfficeUpdate(PermissionRequiredMixin, UpdateView):
    model = Office
    fields = [
        'office_name', 'office_notes', 'office_houses_id', 'office_is_store'
    ]
    permission_required = 'catalog.change_office'
    success_url = reverse_lazy('office')


class OfficeDelete(PermissionRequiredMixin, DeleteView):
    model = Office
    success_url = reverse_lazy('office')
    permission_required = 'catalog.delete_office'
#######################################################################################

# DEPARTMENT Class
class DepartmentListView(PermissionRequiredMixin, generic.ListView):
    model = Department
    fields = '__all__'
    permission_required = 'catalog.view_department'
    #LoginRequiredMixin
    paginate_by = 50


class DepartmentCreate(PermissionRequiredMixin, CreateView):
    model = Department
    fields = '__all__'
    permission_required = 'catalog.add_department'
    success_url = reverse_lazy('department')


class DepartmentUpdate(PermissionRequiredMixin, UpdateView):
    model = Department
    fields = [
        'department_name', 'department_notes', 'department_region_id',
        'department_parent_id'
    ]
    permission_required = 'catalog.change_department'
    success_url = reverse_lazy('department')


class DepartmentDelete(PermissionRequiredMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('department')
    permission_required = 'catalog.delete_department'
#######################################################################################

#POSITION Class
class PositionListView(PermissionRequiredMixin, generic.ListView):
    model = Position
    fields = '__all__'
    permission_required = 'catalog.view_position'
    paginate_by = 50


class PositionCreate(PermissionRequiredMixin, CreateView):
    model = Position
    fields = '__all__'
    permission_required = 'catalog.add_position'
    success_url = reverse_lazy('position')


class PositionUpdate(PermissionRequiredMixin, UpdateView):
    model = Position
    fields = [
        'position_name', 'position_notes', 'position_department_id'
    ]
    permission_required = 'catalog.change_position'
    success_url = reverse_lazy('position')


class PositionDelete(PermissionRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('position')
    permission_required = 'catalog.delete_position'
#######################################################################################

#EMPLOYEE
class EmployeeListView(PermissionRequiredMixin, generic.ListView):
    model = Employee
    fields = '__all__'
    permission_required = 'catalog.view_employee'
    paginate_by = 50
    

class EmployeeCreate(PermissionRequiredMixin, CreateView):
    model = Employee
    fields = '__all__'
    permission_required = 'catalog.add_employee'
    success_url = reverse_lazy('employee')


class EmployeeUpdate(PermissionRequiredMixin, UpdateView):
    model = Employee
    fields = [
        'employee_lastname', 
        'employee_firstname',  
        'employee_middlename',
        'employee_email',
        'employee_position_id', 
        'employee_office_id',
        'employee_phone_work',
        'employee_note',
        'employee_full_fio', 
        'employee_is_chief',
        'employee_is_respons'
    ]
    permission_required = 'catalog.change_employee'
    success_url = reverse_lazy('employee')


class EmployeeDelete(PermissionRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee')
    permission_required = 'catalog.delete_employee'
#######################################################################################

#MCTYPE
class MCTypeListView(PermissionRequiredMixin, generic.ListView):
    model = MCType
    fields = '__all__'
    permission_required = 'catalog.view_mctype'
    paginate_by = 50
    

class MCTypeCreate(PermissionRequiredMixin, CreateView):
    model = MCType
    fields = '__all__'
    permission_required = 'catalog.add_mctype'
    success_url = reverse_lazy('mctype')


class MCTypeUpdate(PermissionRequiredMixin, UpdateView):
    model = MCType
    fields = [
        'wtype_name',
        'wtype_notes'
    ]
    permission_required = 'catalog.change_mctype'
    success_url = reverse_lazy('mctype')


class MCTypeDelete(PermissionRequiredMixin, DeleteView):
    model = MCType
    success_url = reverse_lazy('mctype')
    permission_required = 'catalog.delete_mctype'
#######################################################################################

#HARDWARE
class HardwareListView(PermissionRequiredMixin, generic.ListView):
    model = Hardware
    fields = '__all__'
    permission_required = 'catalog.view_hardware'
    paginate_by = 50
    

class HardwareCreate(PermissionRequiredMixin, CreateView):
    model = Hardware    
    permission_required = 'catalog.add_hardware'
    success_url = reverse_lazy('hardware')
    form_class = HardwareForm


class HardwareUpdate(PermissionRequiredMixin, UpdateView):
    model = Hardware    
    permission_required = 'catalog.change_hardware'
    success_url = reverse_lazy('hardware')
    form_class = HardwareForm


class HardwareDelete(PermissionRequiredMixin, DeleteView):
    model = Hardware
    success_url = reverse_lazy('hardware')
    permission_required = 'catalog.delete_hardware'
#######################################################################################

#RELOFFICERESP
class RelOfficeRespListView(PermissionRequiredMixin, generic.ListView):
    model = RelOfficeResp
    fields = '__all__'
    permission_required = 'catalog.view_relofficeresp'
    paginate_by = 50

class RelOfficeRespCreate(PermissionRequiredMixin, CreateView):
    model = RelOfficeResp    
    permission_required = 'catalog.add_relofficeresp'
    success_url = reverse_lazy('relofficeresp')
    form_class = RelOfficeRespForm


class RelOfficeRespUpdate(PermissionRequiredMixin, UpdateView):
    model = RelOfficeResp    
    permission_required = 'catalog.change_relofficeresp'
    success_url = reverse_lazy('relofficeresp')
    form_class = RelOfficeRespForm


class RelOfficeRespDelete(PermissionRequiredMixin, DeleteView):
    model = RelOfficeResp
    success_url = reverse_lazy('relofficeresp')
    permission_required = 'catalog.delete_relofficeresp'
#######################################################################################