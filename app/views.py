import os
from django.shortcuts import get_object_or_404, redirect, render 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import User,auth
from django.urls import reverse
from .models import Coding, Employees, Project,Tool
from .forms import CodingForm, EmployeeProjectsForm, EmployeesForm, ProjectForm, ToolForm
from django.core.paginator import Paginator
import pdfkit
from .pdfkit_config import config
""" config=pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") """



def register(request):
     if request.method == "POST":
         username = request.POST['fullname']
         email = request.POST['email']
         password = request.POST['pass']
         confirm_password = request.POST['cpass']
         if password == confirm_password:
             if User.objects.filter(username=username).exists():
                 print("Username already exists")
                 messages.error(request, "Username already exists")
                 return redirect('register')
             else:
                 user = User.objects.create_user(username=username, email=email, password=password)
                 user.set_password(password)
                 user.save()
                 print("Successfully registered")
                 messages.success(request, "Successfully registered")
                 return redirect('login')
         else:
            print("Passwords do not match")
            messages.error(request, "Passwords do not match")
            return redirect('register')
     else:
         print("This is not a POST method")
         return render(request, "register.html")
     

def login(request):
     if request.method == "POST":
        username = request.POST['fullname']
        password = request.POST['pass']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard-dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Username or Password! Please try again.')
            return redirect('login') 
     else:
         return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect("login")  

def index(request):
    emp=Employees.objects.all()
    project=Project.objects.all()
    code=Coding.objects.all()
    tools=Tool.objects.all()

    total_emp=emp.count()
    total_project=project.count()
    total_code=code.count()
    total_tools=tools.count()

    context={
        'total_emp':total_emp,
        'total_project':total_project,
        'total_code':total_code,
        'total_tools':total_tools,


    }
    return render(request, 'dashboard/dashboard.html',context)

"""   ------------------------------- Employee Page------------------------------------ """


def employee(request):
    employee=Employees.objects.all()
    paginator=Paginator(employee,4)
    page_num=request.GET.get('page')
    employee_data =paginator.get_page(page_num)
    
    context ={
         "employee" : employee_data,
     }
     
    return render(request,'dashboard/employee.html' , context) 


def employee_add(request):
    form = EmployeesForm()
    if request.method == "POST":
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-employee')
    context = {
        "form": form
    }
    return render(request, 'dashboard/employee_add.html', context)


def employee_projects(request, employee_id):
    employee = get_object_or_404(Employees, pk=employee_id)
    projects = Project.objects.all()

    if request.method == 'POST':
        form = EmployeeProjectsForm(request.POST)
        if form.is_valid():
            selected_projects = form.cleaned_data['projects']
            employee.projects.set(selected_projects)  
            return redirect('dashboard-employee')  

    else:
        form = EmployeeProjectsForm()

    context = {
        'employee': employee,
        'projects': projects,
        'form': form,
    }

    return render(request, 'dashboard/employee_projects.html', context)


def employee_edit(request, pk):
    employee = Employees.objects.get(id=pk)
    if request.method == 'POST':
        form = EmployeesForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('dashboard-employee')  
    else:
        form = EmployeesForm(instance=employee)

    context = {
        'form': form,
    }

    return render(request, 'dashboard/employee_edit.html', context)


def employee_delete(request, pk):
    employee = Employees.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('dashboard-employee')
    context = {
        'employee': employee
    }
    return render(request, 'dashboard/employee_delete.html', context)


def resume(request, pk):
    employee = Employees.objects.get(id=pk)

    return render(request, 'dashboard/Resume.html', {'employee': employee})
    

""" def resume_download(request,pk):
    options = {
        'page-size': 'A4',  
        'encoding': 'UTF-8',
    }

    employee = Employees.objects.get(id=pk)
    pdf =  pdfkit.from_url(request.build_absolute_uri(reverse('dashboard-Resume',args=[pk])), False, configuration=config, options=options )
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.name}" ''s Resume.pdf"'
    return response
 """
def resume_download(request, pk):
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }
    
    employee = get_object_or_404(Employees, id=pk)
    resume_url = request.build_absolute_uri(reverse('dashboard-Resume', args=[pk]))
    config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf = pdfkit.from_file(resume_url, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{employee.name}\'s Resume.pdf"'
    return response


"""   ------------------------------- Coding Page------------------------------------ """


def coding_skills(request):
     coding_details=Coding.objects.all()
     paginator=Paginator(coding_details,4)
     page_num=request.GET.get('page')
     coding_data =paginator.get_page(page_num)
     context = {
        "coding_details": coding_data,
    } 
     return render(request, 'dashboard/coding_skills.html',context)


def coding_add(request):
    form = CodingForm()
    if request.method == "POST":
        form = CodingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coding_skills')
    context = {
        "form": form
    }
    return render(request, 'dashboard/coding_add.html', context)


def coding_edit(request, pk):
    coding_details = Coding.objects.get(id=pk)
    if request.method == 'POST':
        form = CodingForm(request.POST, instance=coding_details)
        if form.is_valid():
            form.save()
            return redirect('coding_skills')  
    else:
        form = CodingForm(instance=coding_details)

    context = {
        'form': form,
    }

    return render(request, 'dashboard/coding_edit.html', context)


def coding_delete(request, pk):
    coding_details = Coding.objects.get(id=pk)
    if request.method == 'POST':
        coding_details.delete()
        return redirect('coding_skills')
    context = {
        'coding_details': coding_details
    }
    return render(request, 'dashboard/coding_delete.html', context)


"""------------------------------- Tools Page------------------------------------ """


def tools(request):
     tools=Tool.objects.all()
     paginator=Paginator(tools,4)
     page_num=request.GET.get('page')
     tools_data =paginator.get_page(page_num)
     context = {
        "tools": tools_data,
    } 
     return render(request, 'dashboard/tools.html',context)


def tools_add(request):
    form = ToolForm()
    if request.method == "POST":
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tools')
    context = {
        "form": form
    }
    return render(request, 'dashboard/tools_add.html', context)


def tools_edit(request, pk):
    tools = Tool.objects.get(id=pk)
    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tools)
        if form.is_valid():
            form.save()
            return redirect('tools')  
    else:
        form = ToolForm(instance=tools)

    context = {
        'form': form,
    }

    return render(request, 'dashboard/tools_edit.html', context)


def tools_delete(request, pk):
    tools = Tool.objects.get(id=pk)
    if request.method == 'POST':
        tools.delete()
        return redirect('tools')
    context = {
        'tools': tools
    }
    return render(request, 'dashboard/tools_delete.html', context)



"""   ------------------------------- Project Page------------------------------------ """

    
def project(request):
    projects = Project.objects.all()
    paginator=Paginator(projects,4)
    page_num=request.GET.get('page')
    project_data =paginator.get_page(page_num)
    context = {
        "projects": project_data,
    } 
    return render(request, 'dashboard/project.html', context)

def project_add(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-project')
    context = {
        "form": form
    }
    return render(request, 'dashboard/project_add.html', context)


def project_edit(request, pk):
    projects = Project.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=projects)
        if form.is_valid():
            form.save()
            return redirect('dashboard-project')  
    else:
        form = ProjectForm(instance=projects)

    context = {
        'form': form,
    }

    return render(request, 'dashboard/project_edit.html', context)


def project_delete(request, pk):
    projects = Project.objects.get(id=pk)
    if request.method == 'POST':
        projects.delete()
        return redirect('dashboard-project')
    context = {
        'projects': projects
    }
    return render(request, 'dashboard/project_delete.html', context)


