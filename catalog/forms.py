from django import forms
from django.forms import ModelForm, CharField, ComboField
from catalog.models import *
from django.shortcuts import get_object_or_404


class RelOfficeRespForm(ModelForm):
    class Meta:
        model = RelOfficeResp
        fields = [
            'roe_id',
            'roe_office_id',
            'roe_employee_id',
        ]


class RelHardEmpForm(ModelForm):
    class Meta:
        model = RelHardEmp
        fields = [
            'relhe_employee_id',
            'relhe_whard_id',
        ]

    def __init__(self, *args, **kwargs):
        kw = args
        super(RelHardEmpForm, self).__init__(*args, **kwargs)
        self.fields['relhe_employee_id'].queryset = Employee.objects.filter(
            pk=14)
            


class HardwareForm(ModelForm):
    #whard_mol_employee_id = forms.ModelChoiceField(
    #    queryset=Employee.objects.filter(employee_is_mol=True,
    #    employee_position_id__position_department_id__department_region_id__pk__exact=self.whard_region_id),
    #    empty_label='------',
    #    label='МО')
    #whard_office_id = forms.ModelChoiceField(queryset=Office.objects.filter(office_houses_id__houses_region_id__pk__exact=54),
    #    empty_label='------', label='Офис')

    #def __init__(self,*args,**kwargs):
    #    super (HardwareForm,self ).__init__(*args,**kwargs) # populates the post
    #    self.fields['whard_mol_employee_id'].queryset = Employee.objects.filter(employee_is_mol=True,
    #            employee_position_id__position_department_id__department_region_id__pk__exact=54)
    #    #self.fields['client'].queryset = Client.objects.filter(company=company)

    class Meta:
        model = Hardware
        fields = [
            'whard_id',
            'whard_inumber',
            'whard_fnumber',
            'whard_wcat_id',
            'whard_wtype_id',
            'whard_name',
            'whard_date_of_adoption',
            'whard_initial_cost',
            'whard_residual_value',
            'whard_region_id',
            'whard_office_id',
            'whard_mol_employee_id',
            'whard_note',
            'whard_archiv',
        ]
        widgets = {
            'whard_date_of_adoption': forms.DateInput(attrs={'type': 'date'}),
            'whard_initial_cost': forms.NumberInput(attrs={'type': 'number'}),
        }
