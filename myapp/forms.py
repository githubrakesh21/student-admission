from .models import Student

from .models import Student,Admin

from django.forms import ModelForm
from django import forms 



class LoginForm(ModelForm):
    class Meta:
        model =Student
        fields=["email","password"]

class StudentForm(LoginForm):
    class Meta(LoginForm.Meta):
        model =Student
        fields=LoginForm.Meta.fields+["id","first_name","last_name","mobile","qualification","gender","address"]
        widgets={
            "gender":forms.RadioSelect(attrs={'class':'radio'}),
        }
    
class AdminForm(ModelForm):
    class Meta:
        model =Admin
        fields="__all__"