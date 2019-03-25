from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard')
]

#HOUSE
urlpatterns += [
    path('house/', views.HouseListView.as_view(), name='house'),
    path('house/create/', views.HouseCreate.as_view(), name='house_create'),
    path('house/<int:pk>/update/', views.HouseUpdate.as_view(), name='house_update'),
    path('house/<int:pk>/delete/', views.HouseDelete.as_view(), name='house_delete'),
]

#OFFICE
urlpatterns += [
    path('office/', views.OfficeListView.as_view(), name='office'),  
    path('office/create/', views.OfficeCreate.as_view(), name='office_create'),
    path('office/<int:pk>/update/', views.OfficeUpdate.as_view(), name='office_update'),
    path('office/<int:pk>/delete/', views.OfficeDelete.as_view(), name='office_delete'),
]

#DEPARTMENT
urlpatterns += [
    path('department/', views.DepartmentListView.as_view(), name='department'),
    path('department/create/', views.DepartmentCreate.as_view(), name='department_create'),
    path('department/<int:pk>/update/', views.DepartmentUpdate.as_view(), name='department_update'),
    path('department/<int:pk>/delete/', views.DepartmentDelete.as_view(), name='department_delete'), 
]

#POSITION
urlpatterns += [
    path('position/', views.PositionListView.as_view(), name='position'),
    path('position/create/', views.PositionCreate.as_view(), name='position_create'),
    path('position/<int:pk>/update/', views.PositionUpdate.as_view(), name='position_update'),
    path('position/<int:pk>/delete/', views.PositionDelete.as_view(), name='position_delete'), 
]

#EMPLOYEE
urlpatterns += [
    path('employee/', views.EmployeeListView.as_view(), name='employee'),
    path('employee/create/', views.EmployeeCreate.as_view(), name='employee_create'),
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee_delete'), 
]

#MCTYPE
urlpatterns += [
    path('mctype/', views.MCTypeListView.as_view(), name='mctype'),
    path('mctype/create/', views.MCTypeCreate.as_view(), name='mctype_create'),
    path('mctype/<int:pk>/update/', views.MCTypeUpdate.as_view(), name='mctype_update'),
    path('mctype/<int:pk>/delete/', views.MCTypeDelete.as_view(), name='mctype_delete'), 
]

#HARDWARE
urlpatterns += [
    path('hardware/', views.HardwareListView.as_view(), name='hardware'),
    path('hardware/create/', views.HardwareCreate.as_view(), name='hardware_create'),
    path('hardware/<int:pk>/update/', views.HardwareUpdate.as_view(), name='hardware_update'),
    path('hardware/<int:pk>/delete/', views.HardwareDelete.as_view(), name='hardware_delete'), 
]

#REL_OFFICE_EMPLOYEE
urlpatterns += [
    path('relofficeresp/', views.RelOfficeRespListView.as_view(), name='relofficeresp'),
    path('relofficeresp/create/', views.RelOfficeRespCreate.as_view(), name='relofficeresp_create'),
    path('relofficeresp/<int:pk>/update/', views.RelOfficeRespUpdate.as_view(), name='relofficeresp_update'),
    path('relofficeresp/<int:pk>/delete/', views.RelOfficeRespDelete.as_view(), name='relofficeresp_delete'),
]