from django.shortcuts import render
from django.urls import reverse_lazy
from django import template
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import House, Office, Department, Position, Employee, MCCat, MCType, Region
from catalog.models import RelHardEmp, RelOfficeResp, Hardware
from .forms import *

from django.views.generic import ListView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission

#from .tables import HouseTable
#from .filters import HouseFilter


class _baseCreateFormView(PermissionRequiredMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class _baseUpdateFormView(PermissionRequiredMixin, UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def get_user_regions(user):
    permissions = Permission.objects.filter(
        user=user) | Permission.objects.filter(group__user=user)
    user_regions = []
    for p in permissions:
        if p.codename in ['22', '24', '38', '42', '54', '55', '70']:
            user_regions.append(p.codename)
    return user_regions


#######################################################################################


# HOUSE Class
class HouseListView(PermissionRequiredMixin, generic.ListView):
    model = House
    fields = '__all__'
    permission_required = 'catalog.view_house'

    #LoginRequiredMixin
    #paginate_by = 10

    #def get_queryset(self):
    #    return House.objects.filter(
    #        houses_region_id__in=get_user_regions(self.request.user))

    def get_context_data(self, **kwargs):
        house_list = House.objects.all()

        search_text = ""
        search_region = ""

        context = super().get_context_data(**kwargs)

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            house_list = house_list.filter(
                houses_region_id__pk__exact=search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            house_list = house_list.filter(
                Q(houses_name__icontains=search_text)
                | Q(houses_rem__icontains=search_text)
                | Q(houses_region_id__region_name__icontains=search_text))

        house_list = house_list.filter(
            houses_region_id__in=get_user_regions(self.request.user))

        get_dict_copy = self.request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {
            'house_list': house_list,
            'params': params,
            'search_text': search_text,
            'search_region': search_region,
        }
        return context


class HouseDetailView(LoginRequiredMixin, generic.DetailView):
    model = House


class HouseCreate(_baseCreateFormView):
    model = House
    #fields = '__all__'
    permission_required = 'catalog.add_house'
    success_url = reverse_lazy('house')
    form_class = HouseForm


class HouseUpdate(_baseUpdateFormView):
    model = House
    #fields = ['houses_name', 'houses_rem', 'houses_region_id']
    permission_required = 'catalog.change_house'
    success_url = reverse_lazy('house')
    form_class = HouseForm


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
    paginate_by = 100

    @property
    def get_total_list_count(self):
        return model.Office.objects.all().count()

    #def get_queryset(self):
    #    return Office.objects.filter(
    #        office_houses_id__houses_region_id__in=get_user_regions(
    #            self.request.user))

    def get_context_data(self, **kwargs):
        office_list = Office.objects.all()

        search_text = ""
        search_region = ""

        context = super().get_context_data(**kwargs)

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            office_list = office_list.filter(
                office_houses_id__houses_region_id__pk__exact=search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            office_list = office_list.filter(
                Q(office_name__icontains=search_text)
                | Q(office_notes__icontains=search_text))

        office_list = office_list.filter(
            office_houses_id__houses_region_id__in=get_user_regions(
                self.request.user))

        get_dict_copy = self.request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {
            'office_list': office_list,
            'params': params,
            'search_text': search_text,
            'search_region': search_region,
        }
        return context


class OfficeCreate(_baseCreateFormView):
    model = Office
    #fields = '__all__'
    permission_required = 'catalog.add_office'
    success_url = reverse_lazy('office')
    form_class = OfficeForm


class OfficeUpdate(_baseUpdateFormView):
    model = Office
    #fields = [
    #    'office_name', 'office_notes', 'office_houses_id', 'office_is_store'
    #]
    permission_required = 'catalog.change_office'
    success_url = reverse_lazy('office')
    form_class = OfficeForm


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

    #def get_queryset(self):
    #    return Department.objects.filter(
    #        department_region_id__in=get_user_regions(self.request.user))

    def get_context_data(self, **kwargs):
        department_list = Department.objects.all()

        search_text = ""
        search_region = ""

        context = super().get_context_data(**kwargs)

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            department_list = department_list.filter(
                department_region_id__pk__exact=search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            department_list = department_list.filter(
                Q(department_name__icontains=search_text)
                | Q(department_notes__icontains=search_text)
                | Q(department_region_id__region_name__icontains=search_text))

        department_list = department_list.filter(
            department_region_id__in=get_user_regions(self.request.user))

        get_dict_copy = self.request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {
            'department_list': department_list,
            'params': params,
            'search_text': search_text,
            'search_region': search_region,
        }
        return context


class DepartmentCreate(_baseCreateFormView):
    model = Department
    #fields = '__all__'
    permission_required = 'catalog.add_department'
    success_url = reverse_lazy('department')
    form_class = DepartmentForm


class DepartmentUpdate(_baseUpdateFormView):
    model = Department
    #fields = [
    #    'department_name', 'department_notes', 'department_region_id',
    #    'department_parent_id'
    #]
    permission_required = 'catalog.change_department'
    success_url = reverse_lazy('department')
    form_class = DepartmentForm


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

    #def get_queryset(self):
    #    return Position.objects.filter(
    #        position_department_id__department_region_id__in=get_user_regions(
    #            self.request.user))

    def get_context_data(self, **kwargs):
        position_list = Position.objects.all()

        search_text = ""
        search_region = ""

        context = super().get_context_data(**kwargs)

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            position_list = position_list.filter(
                position_department_id__department_region_id__pk__exact=
                search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            position_list = position_list.filter(
                Q(position_name__icontains=search_text)
                | Q(position_notes__icontains=search_text)
                |
                Q(position_department_id__department_region_id__region_name__contains
                  =search_text))

        position_list = position_list.filter(
            position_department_id__department_region_id__in=get_user_regions(
                self.request.user))

        get_dict_copy = self.request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {
            'position_list': position_list,
            'params': params,
            'search_text': search_text,
            'search_region': search_region,
        }
        return context


class PositionCreate(_baseCreateFormView):
    model = Position
    #fields = '__all__'
    permission_required = 'catalog.add_position'
    success_url = reverse_lazy('position')
    form_class = PositionForm


class PositionUpdate(_baseUpdateFormView):
    model = Position
    #fields = ['position_name', 'position_notes', 'position_department_id']
    permission_required = 'catalog.change_position'
    success_url = reverse_lazy('position')
    form_class = PositionForm


class PositionDelete(PermissionRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('position')
    permission_required = 'catalog.delete_position'


#######################################################################################


#EMPLOYEE
class EmployeeListView(PermissionRequiredMixin, ListView):
    model = Employee
    fields = '__all__'
    permission_required = 'catalog.view_employee'
    paginate_by = 100

    def get_queryset(self):
        search_region = ""
        search_text = ""

        employee_list = Employee.objects.all()
        employee_list = employee_list.filter(
            employee_position_id__position_department_id__department_region_id__in
            =get_user_regions(self.request.user))

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']
            employee_list = employee_list.filter(
                employee_position_id__position_department_id__department_region_id__pk__exact
                =search_region)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            employee_list = employee_list.filter(
                Q(employee_lastname__icontains=search_text)
                | Q(employee_note__icontains=search_text)
                | Q(employee_full_fio__icontains=search_text)
                |
                Q(employee_position_id__position_department_id__department_region_id__region_name__icontains
                  =search_text))

        return employee_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_text = ""
        search_region = ""
        user_regions = ""
        user_regions = get_user_regions(self.request.user)

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']

        if 'region' in self.request.GET:
            search_region = self.request.GET['region']

        context['search_text'] = search_text
        context['search_region'] = search_region
        context['user_regions'] = user_regions

        employee_list = EmployeeListView.get_queryset(self)

        return context


class EmployeeCreate(_baseCreateFormView):
    model = Employee
    #fields = '__all__'
    permission_required = 'catalog.add_employee'
    success_url = reverse_lazy('employee')
    form_class = EmployeeForm


class EmployeeUpdate(_baseUpdateFormView):
    model = Employee
    #fields = [
    #    'employee_lastname', 'employee_firstname', 'employee_middlename',
    #    'employee_email', 'employee_position_id', 'employee_office_id',
    #    'employee_phone_work', 'employee_note', 'employee_full_fio',
    #    'employee_is_chief', 'employee_is_respons'
    #]
    permission_required = 'catalog.change_employee'
    success_url = reverse_lazy('employee')
    form_class = EmployeeForm


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
    fields = ['wtype_name', 'wtype_notes']
    permission_required = 'catalog.change_mctype'
    success_url = reverse_lazy('mctype')


class MCTypeDelete(PermissionRequiredMixin, DeleteView):
    model = MCType
    success_url = reverse_lazy('mctype')
    permission_required = 'catalog.delete_mctype'


#######################################################################################

#MCAT
class MCCatListView(PermissionRequiredMixin, generic.ListView):
    model = MCCat
    fields = '__all__'
    permission_required = 'catalog.view_mccat'
    paginate_by = 50


class MCCatCreate(PermissionRequiredMixin, CreateView):
    model = MCCat
    fields = '__all__'
    permission_required = 'catalog.add_mccat'
    success_url = reverse_lazy('mccat')


class MCCatUpdate(PermissionRequiredMixin, UpdateView):
    model = MCCat
    fields = ['wcatname','wcatnotes',]
    permission_required = 'catalog.change_mccat'
    success_url = reverse_lazy('mccat')


class MCCatDelete(PermissionRequiredMixin, DeleteView):
    model = MCCat
    success_url = reverse_lazy('mccat')
    permission_required = 'catalog.delete_mccat'


#######################################################################################