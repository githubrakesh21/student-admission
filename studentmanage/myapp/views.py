from django.shortcuts import render,HttpResponse
from urllib.parse import urlparse, parse_qs
import re
from .models import Student,Admin,Credentials
from rest_framework.views import APIView
from .forms import StudentForm,AdminForm,LoginForm
from .models import Credentials,Admin,Student
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def emailvalidation(email):
    validator = r'^[a-zA-Z0-9][a-zA-Z0-9\.\-_]+@[a-z]+\.[a-z]{2,3}$'
    if re.match(validator,email):
        return True
    else:
        return False

def mobilevalidation(mobile):
    if len(mobile) == 10 and mobile.isdigit():
        return True
    else:
        return False
def namevalidation(fullname):
    if fullname.isalpha():
        return True
    else:
        return False
def details_validation(email,mobile,fullname):
    message = []
    if not emailvalidation(email):
        message.append('email')
    if not mobilevalidation(mobile):
        message.append('mobile')
    if not namevalidation(fullname):
        message.append('name')
    if message:
        return 'invalid '+",".join(message)+'!!' 
    else :
        return message


def Welcome(request):
    return render(request,'home.html')
class StudentView():
    def get_details(request):
        id = int(request.GET.get('id'))
        # print(type(id))
        student_dict = Student.objects.values().get(id=id)
        context= {'data' :student_dict}
        context['is_student_view'] = False
        return render(request,'summary_view.html',context)
        pass
    def _summary(email):
        Student_obj = Student.objects.values().get(email=email)
        return Student_obj

    def register(request):
        context = {}
        context['form_name'] = 'Student'
        context['form'] = StudentForm
        if request.method == 'POST':
            student_data = StudentForm(request.POST)
            # form = UserRegisterForm(request.POST)
            if student_data.is_valid():
                # print('issave')
                email = request.POST['email']
                password = request.POST['password']
                mobile_number = request.POST['mobile']
                full_name = request.POST['first_name'].strip() + request.POST['last_name'].strip()
                error_message = details_validation(email,mobile_number,full_name)
                # print(error_message)
                if error_message:
                    # print('coming')
                    context['error_message'] = error_message
                else:
                    # print('no')
                    student_data.save()
                    student_id = Student.objects.filter(email=email).values_list('id',flat=True)[0]
                    student_obj  = Credentials.objects.create(email=email,password=password,student_id_id=student_id)
                    context['success'] = request.POST['first_name']+' '+'added Successfully!!'
                # print('bye')
        return render(request,'register.html',context)
    
    def login(request):
        context={}
        context['form'] =  LoginForm
        if request.method == 'POST':
            email = request.POST['email']
            password= request.POST['password']
            # print(email)
            # print('hi')
            try :
                # print('hel0')
                if not email or not (Credentials.objects.get(email=email)):
                    # print('i')
                    context['message'] = 'invalid Credentials'
                    raise ValueError('invalid Credentials')
                else :
                    # print('k')
                    loged_details = Credentials.objects.values().get(email=email,password=password)
                    # print(loged_details)
                    if  loged_details['is_admin'] :
                        # print('j')
                        admin_student_dict = Admin_view.get_details()
                        # print('m')
                        context['data'] = admin_student_dict
                        # print(admin_student_dict)
                        return render(request,'admin.html',context)
                    # praveen
                    else :
                        student_obj = StudentView._summary(email)
                        context['data'] = student_obj
                        context['is_student_view'] = True
                        return render(request,'summary_view.html',context)
            except Exception as e:
                context['message'] = 'invalid Credentials'
                print(e)

        return render(request,'login.html',context)
    
class Admin_view():

    def get_details():
        students_details  = Student.objects.all().values()
        # context = {}
        # print(students_details[0])
        # context ["data"] = students_details
        for row in students_details:
            row['link'] = 'http:'+'//127.0.0.1:8000/login/admin/?id='+str(row['id'])

        return students_details
    
    def post_details(request):

        context ={}
        context['form_name'] = 'Admin'
        context ["form"] = AdminForm

        if request.method == 'POST':

            admin_details = request.POST

            form = AdminForm(admin_details)

            if form.is_valid():
                email = admin_details['email']
                mobile_number = admin_details['mobile']
                full_name = admin_details['first_name'].strip() + admin_details['last_name'].strip()
                error_message = details_validation(email,mobile_number,full_name)
                if error_message:
                    context['error_message'] = error_message
                else:
                    form.save()
                    admin_id = Admin.objects.filter(email=email).values_list('id',flat=True)[0]
                    password = admin_details['password']
                    student_obj  = Credentials.objects.create(email=email,password=password,is_admin=True,admin_id_id=admin_id)
                
                    context['success'] = admin_details['first_name']+" is registered succefully...!"
        
        return  render(request, "register.html", context)
