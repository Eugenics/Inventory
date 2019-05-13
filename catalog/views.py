from django.shortcuts import render
from refs.models import House, Office, Department, Position, Employee, MCCat, MCType, Region
from catalog.models import RelHardEmp, RelOfficeResp, Hardware
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import *

from django.http import JsonResponse

from django.core import serializers
from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView
from django.views import generic


def get_user_regions(user):
    permissions = Permission.objects.filter(
        user=user) | Permission.objects.filter(group__user=user)
    user_regions = []
    for p in permissions:
        if p.codename in ['22', '24', '38', '42', '54', '55', '70']:
            user_regions.append(p.codename)
    return user_regions


#AJAX VIEW
@login_required
def update_mol_by_region(request):
    region_id = request.GET.get('region_id', None)
    mol_list = list(
        Employee.objects.filter(
            employee_position_id__position_department_id__department_region_id__pk__exact
            =region_id,
            employee_is_mol=True).values('employee_id', 'employee_full_fio'))
    #print('123')
    return JsonResponse(mol_list, safe=False)


@login_required
def update_department_by_region(request):
    region_id = request.GET.get('region_id', None)
    department_list = list(
        Department.objects.filter(
            department_region_id__exact=region_id).values(
                'department_id', 'department_name'))
    return JsonResponse(department_list, safe=False)


@login_required
def update_office_by_region(request):
    region_id = request.GET.get('region_id', None)
    office_list = list(
        Office.objects.filter(
            office_houses_id__houses_region_id__pk__exact=region_id).values(
                'office_id', 'office_name'))
    return JsonResponse(office_list, safe=False)


@login_required
def update_position_by_region(request):
    region_id = request.GET.get('region_id', None)
    position_list = list(
        Position.objects.filter(
            position_department_id__department_region_id__pk__exact=region_id).
        values('position_id', 'position_name', 'position_department_id__department_name'))
    return JsonResponse(position_list, safe=False)


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


#HARDWARE
class HardwareListView(PermissionRequiredMixin, ListView):
    model = Hardware
    fields = '__all__'
    permission_required = 'catalog.view_hardware'
    paginate_by = 50

    def get_queryset(self):
        search_region = ""
        search_text = ""

        hardware_list = Hardware.objects.all()
        hardware_list = hardware_list.filter(
            whard_region_id__in=get_user_regions(self.request.user))

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            hardware_list = hardware_list.filter(
                whard_region_id__pk__exact=search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            hardware_list = hardware_list.filter(
                Q(whard_inumber__icontains=search_text)
                | Q(whard_name__icontains=search_text)
                | Q(whard_note__icontains=search_text)
                | Q(whard_region_id__region_name__icontains=search_text)
                | Q(whard_office_id__office_name__icontains=search_text))

        return hardware_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_region = ""
        search_text = ""

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']

        context['search_text'] = search_text
        context['search_region'] = search_region

        hardware_list = HardwareListView.get_queryset(self)

        #hardware_list = hardware_list.filter(
        #    whard_region_id__in=get_user_regions(self.request.user))
        #get_dict_copy = self.request.GET.copy()
        #params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        return context


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


#RELHARDEMP
class RelHardEmpListView(PermissionRequiredMixin, generic.ListView):
    fields = '__all__'
    permission_required = 'catalog.view_employee'
    paginate_by = 50

    def get_queryset(self):
        self.relhe_employee_id = get_object_or_404(
            Employee, employee_id=self.kwargs['employee_id'])
        return RelHardEmp.objects.filter(
            relhe_employee_id__pk=self.relhe_employee_id.employee_id)
        #return RelHardEmp.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relhe_employee_id'] = self.relhe_employee_id
        context['employee_pk'] = self.relhe_employee_id.pk
        return context


class RelHardEmpCreate(PermissionRequiredMixin, CreateView):
    model = RelHardEmp
    permission_required = 'catalog.add_relhardemp'
    form_class = RelHardEmpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_pk'] = self.kwargs['employee_id']
        return context

    def get_success_url(self):
        return reverse_lazy('relhardemp',
                            kwargs={
                                'employee_id': self.kwargs['employee_id'],
                            })


class RelHardEmpUpdate(PermissionRequiredMixin, UpdateView):
    model = RelHardEmp
    permission_required = 'catalog.change_relhardemp'
    success_url = reverse_lazy('relhardemp')
    form_class = RelHardEmpForm

    def get_success_url(self):
        return reverse_lazy('relhardemp',
                            kwargs={
                                'employee_id': self.kwargs['employee_id'],
                            })


class RelHardEmpDelete(PermissionRequiredMixin, DeleteView):
    model = RelHardEmp
    success_url = reverse_lazy('relhardemp')
    permission_required = 'catalog.delete_relhardemp'

    def get_success_url(self):
        return reverse_lazy('relhardemp',
                            kwargs={
                                'employee_id': self.kwargs['employee_id'],
                            })


#######################################################################################
