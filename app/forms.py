from django import forms
from .models import Employees
from .models import Coding_list
from .models import Tool_list
from .models import Coding
from .models import Tool,Technology_list,Project
from ckeditor.widgets import CKEditorWidget

class EmployeesForm(forms.ModelForm):
    coding_skills = forms.ModelMultipleChoiceField(queryset=Coding_list.objects.all(), widget=forms.SelectMultiple)
    tools = forms.ModelMultipleChoiceField(queryset=Tool_list.objects.all(), widget=forms.SelectMultiple)
       
    class Meta:
        model = Employees
        fields = ['id', 'name', 'designation', 'professional_summary', 'coding_skills', 'tools', 'emp_status'] 



class CodingForm(forms.ModelForm):
    coding_skills = forms.ModelMultipleChoiceField(queryset=Coding_list.objects.all(), widget=forms.SelectMultiple)
    class Meta:
        model = Coding
        fields = ['id','emp_name','coding_skills']



class ToolForm(forms.ModelForm):
    tools =  forms.ModelMultipleChoiceField(queryset=Tool_list.objects.all(), widget=forms.SelectMultiple)
    class Meta:
        model= Tool
        fields = ['id','emp_name','tools']


class ProjectForm(forms.ModelForm):
    technology =  forms.ModelMultipleChoiceField(queryset=Technology_list.objects.all(), widget=forms.SelectMultiple)
    roles_responsibilities = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model= Project
        fields = ['id','project_name','technology','description','roles_responsibilities','start_date','end_date','project_status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeProjectsForm(forms.Form):
    projects = forms.ModelMultipleChoiceField( queryset=Project.objects.all(),widget=forms.SelectMultiple,)




