from django import forms
from django.forms import ModelForm
from catalog.models import House, Office, Department, Position, Employee, MCCat, MCType, Region, Hardware,RelOfficeResp


class HardwareForm(ModelForm):
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
            'whard_office_id',
            'whard_note',
            'whard_archiv',
        ]
        widgets = {            
            'whard_date_of_adoption': forms.DateInput(attrs={'type':'date'}),
            'whard_initial_cost': forms.NumberInput(attrs={'type':'number'}),
        }

class RelOfficeRespForm(ModelForm):
    class Meta:
        model = RelOfficeResp
        fields = [
            'roe_id',
            'roe_office_id',
            'roe_employee_id',
        ]