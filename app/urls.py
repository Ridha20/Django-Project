from os import path
from django.urls import path
from . import views


urlpatterns = [
    path('', views.register , name="register"),
    path('login', views.login , name="login"),
    path('dasboard', views.index , name="dashboard-dashboard"),

    path('employee', views.employee , name="dashboard-employee"),
    path('employee_add', views.employee_add, name="dashboard-employee_add"),
    path('employee/<int:employee_id>/employee_projects/', views.employee_projects, name='employee_projects'),
    path('employee_edit/<int:pk>', views.employee_edit, name='dashboard-employee_edit'),
    path('employee_delete/<int:pk>', views.employee_delete,name='dashboard-employee_delete'),
    path('resume/<int:pk>', views.resume,name='dashboard-Resume'),
    path('resume_download/<int:pk>', views.resume_download, name='resume_download'),
    
    

    path('coding_skills', views.coding_skills, name='coding_skills'),
    path('coding_add', views.coding_add, name="dashboard-coding_add"),
    path('coding_edit/<int:pk>', views.coding_edit, name='dashboard-coding_edit'),
    path('coding_delete/<int:pk>', views.coding_delete,name='dashboard-coding_delete'),

    path('tools', views.tools, name='tools'),
    path('tools_add', views.tools_add, name="dashboard-tools_add"),
    path('tools_edit/<int:pk>', views.tools_edit, name='dashboard-tools_edit'),
    path('tools_delete/<int:pk>', views.tools_delete,name='dashboard-tools_delete'),

    path('project', views.project , name="dashboard-project"),
    path('project_add', views.project_add, name="dashboard-project_add"),
    path('project_edit/<int:pk>', views.project_edit, name='dashboard-project_edit'),
    path('project_delete/<int:pk>', views.project_delete,name='dashboard-project_delete'),
    path('logout', views.logout, name='logout'),
    
   
]
