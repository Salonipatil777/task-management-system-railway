from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.


class Employee(models.Model):
    emp_name = models.CharField(max_length=100,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=False)
    email=models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    date_of_join=models.DateTimeField(blank=True, null=True)
    date_of_birth =models.DateTimeField(blank=True, null=True)
    post=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    blood_group=models.CharField(max_length=10)
    image = models.ImageField(upload_to='pics/',default='profile1.jpg')

    def __str__(self):
        return self.emp_name
    
    def get_all_employee(self):
        return Employee.objects.all().order_by('id')
    

class Task(models.Model):
    given_task = models.CharField(max_length=200, null=True)
    task_description = models.CharField(max_length=500, null=True)
    created_date = models.DateField(auto_now_add=True,null=True,blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
    employee_name = models.CharField(max_length=100)
    target_date=models.DateField(auto_now_add=False,null=True,blank=True)
    status = models.CharField(max_length=200, null=True)



    def __str__(self):
        return self.employee_name
    
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)


class Status(models.Model):
    name=models.CharField(max_length=100)
