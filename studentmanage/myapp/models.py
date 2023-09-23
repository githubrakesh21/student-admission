from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
QUALIFICATION_CHOICES=(
    ('ssc','SSC'),
    ('intermediate','INTERMEDIATE'),
    ('degree','DEGREE'),
    ('btech','BTECH')
)

CHOICES = (

        ('m', 'male'),
        ('f','female')

)

 
class Student(models.Model):
    first_name=models.CharField(max_length=30,null=False)
    last_name=models.CharField(max_length=30,null=False)
    gender=models.CharField(max_length=15,choices=CHOICES,blank=False,default='m')
    email= models.EmailField(max_length=70,unique=True,null=False)
    mobile=models.CharField(max_length=15)
    password=models.CharField(max_length=25,null=False)
    qualification=models.CharField(max_length=50,choices=QUALIFICATION_CHOICES,default='ssc')
    address=models.TextField()
    class Meta:
        db_table = 'Student'

class Admin(models.Model):
    first_name=models.CharField(max_length=30,null=False)
    last_name=models.CharField(max_length=30,null=False)
    email= models.EmailField(max_length=70,unique=True,null=False)
    mobile=models.CharField(max_length=15)
    password=models.CharField(max_length=25,null=False)
    class Meta:
        db_table = 'Admin'


class Credentials(models.Model):
    email= models.EmailField(max_length=70,unique=True,null=False)
    password=models.CharField(max_length=25,null=False)
    is_admin=models.BooleanField(default=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,blank=True,null=True)
    admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        db_table = 'Credentials'
    
    
