from django.urls import path
from catalog.views import *
from django.conf.urls import url

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard')
]

#REL_OFFICE_EMPLOYEE
urlpatterns += [
    path('relofficeresp/',
         RelOfficeRespListView.as_view(),
         name='relofficeresp'),
    path('relofficeresp/create/',
         RelOfficeRespCreate.as_view(),
         name='relofficeresp_create'),
    path('relofficeresp/<int:pk>/update/',
         RelOfficeRespUpdate.as_view(),
         name='relofficeresp_update'),
    path('relofficeresp/<int:pk>/delete/',
         RelOfficeRespDelete.as_view(),
         name='relofficeresp_delete'),
]

#REL_HARD_EMP
urlpatterns += [
    path('relhardemp/<employee_id>/',
         RelHardEmpListView.as_view(),
         name='relhardemp'),
    path('relhardemp/<employee_id>/create/',
         RelHardEmpCreate.as_view(),
         name='relhardemp_create'),
    path('relhardemp/<int:pk>/update/',
         RelHardEmpUpdate.as_view(),
         name='relhardemp_update'),
    path('relhardemp/<int:pk>/delete/',
         RelHardEmpDelete.as_view(),
         name='relhardemp_delete'),
]

#HARDWARE
urlpatterns += [
    path('hardware/', HardwareListView.as_view(), name='hardware'),
    path('hardware/create/', HardwareCreate.as_view(), name='hardware_create'),
    path('hardware/<int:pk>/update/',
         HardwareUpdate.as_view(),
         name='hardware_update'),
    path('hardware/<int:pk>/delete/',
         HardwareDelete.as_view(),
         name='hardware_delete'),
]

urlpatterns += [
    url('/update_office_by_region/',
        update_office_by_region,
        name='update_office_by_region'),
    url('/update_mol_by_region/',
        update_mol_by_region,
        name='update_mol_by_region'),
]

urlpatterns += [
    url('/update_department_by_region/',
        update_department_by_region,
        name='update_department_by_region'),
]