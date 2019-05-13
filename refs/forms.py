from django import forms
from django.forms import ModelForm, CharField, ComboField
from .models import *
from django.shortcuts import get_object_or_404
from .funcs import get_user_regions


class HouseForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = House
        fields = [
            'houses_region_id',
            'houses_name',
            'houses_rem',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(HouseForm, self).__init__(*args, **kwargs)
        self.fields['houses_region_id'].queryset = Region.objects.filter(
            pk__in=get_user_regions(user))


class OfficeForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Office
        fields = [
            'office_houses_id',
            'office_name',
            'office_notes',
            'office_is_store',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.fields['office_houses_id'].queryset = House.objects.filter(
            houses_region_id__pk__in=get_user_regions(user))


class DepartmentForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Department
        fields = [
            'department_region_id',
            'department_parent_id',
            'department_name',
            'department_notes',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['department_region_id'].queryset = Region.objects.filter(
            pk__in=get_user_regions(user))
        self.fields[
            'department_parent_id'].queryset = Department.objects.filter(
                department_region_id__in=get_user_regions(user))


class PositionForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Position
        fields = [
            'position_department_id',
            'position_name',
            'position_notes',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields[
            'position_department_id'].queryset = Department.objects.filter(
                department_region_id__in=get_user_regions(user))


class EmployeeForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Employee
        fields = [
            'employee_lastname',
            'employee_firstname',
            'employee_middlename',
            'employee_email',
            'employee_region_id',
            'employee_position_id',
            'employee_office_id',
            'employee_phone_work',
            'employee_note',
            'employee_full_fio',
            'employee_is_chief',
            'employee_is_respons',
            'employee_is_mol',
            'user_id',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['employee_region_id'].queryset = Region.objects.filter(
            pk__in=get_user_regions(user))

        self.fields['employee_position_id'].queryset = Position.objects.filter(
            position_department_id__department_region_id__in=get_user_regions(
                user))

        self.fields['employee_office_id'].queryset = Office.objects.filter(
            office_houses_id__houses_region_id__in=get_user_regions(user))
