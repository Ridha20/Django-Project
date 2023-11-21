from django.db import models
from ckeditor.fields import RichTextField

class Coding_list(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tool_list(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Technology_list(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    


class Coding(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_name= models.CharField(max_length=255,null=True)
    coding_skills = models.ManyToManyField(Coding_list, blank=True)
    
    def __str__(self):
         return self.emp_name


class Tool(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_name= models.CharField(max_length=255,null=True)
    tools = models.ManyToManyField(Tool_list, blank=True)
    
    def __str__(self):
         return self.emp_name



class Project(models.Model):
    PROJECT_CHOICES = [
        ('Active', 'Active'),
        ('Complete', 'Complete'),
    ]

    id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=255, null=True)
    technology=models.ManyToManyField(Technology_list, blank=True)
    description = models.TextField(max_length=1000 , null=True)
    roles_responsibilities = RichTextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    project_status = models.CharField(max_length=20, choices=PROJECT_CHOICES, null=True)

    def __str__(self):
        return self.project_name
    


class Employees(models.Model):
    STATUS_CHOICES = [
        ('current-emp', 'Current-Emp'),
        ('ex-emp', 'Ex-Employee'),
          ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    designation = models.CharField(max_length=255 , null=True)
    professional_summary = RichTextField(null=True)
    coding_skills = models.ManyToManyField(Coding_list, blank=True)
    tools = models.ManyToManyField(Tool_list, blank=True)
    emp_status = models.CharField(max_length=20, choices= STATUS_CHOICES, null=True)
    projects = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.name