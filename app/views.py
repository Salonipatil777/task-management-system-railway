from django.shortcuts import get_object_or_404, redirect, render
from customadmin.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required(login_url='emplogin')
def emplogout(request):
    # if request.method == 'POST':
    #     logout(request)
    #     messages.success(request,"successfully logged out")
    #     return redirect('emplogin')
    # return render(request,'emplogin.html')
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('emplogin')

# @login_required(login_url='emplogin')
# def empdashboard(request):
#     empemail = request.POST.get('empemail')
#     tasks = Task.objects.filter(employee_name=empemail)
#     page = Paginator(tasks,3)
#     page_number = request.GET.get('page')
#     page=page.get_page(page_number)


#     context = {
#         'page': page,
#     }    
       

#     return render(request,'empdashboard.html',context)

def emplogin(request):
    if request.method == 'POST':
        empemail = request.POST.get('empemail')
        emppassword = request.POST.get('emppassword')

        user = authenticate(username=empemail, password=emppassword)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully logged in")
            return redirect('mytasks')
        else:
            messages.error(request,'username or password not correct')
            return redirect('emplogin')
    return render(request,'emplogin.html')


@login_required(login_url='emplogin')
def mytasks(request):
    user = get_object_or_404(User, email=request.user.email)
    employee = get_object_or_404(Employee, user=user)

    tasks = Task.objects.filter(assigned_to=employee).order_by('-id')
    mytaskpage = Paginator(tasks,3)
    page_number = request.GET.get('mytaskpage')
    mytaskpage=mytaskpage.get_page(page_number)

    return render(request, 'mytasks.html', {'mytaskpage': mytaskpage,'employee':employee})

@login_required(login_url='emplogin')
def taskpage(request,id):
    user = get_object_or_404(User, email=request.user.email)
    employee = get_object_or_404(Employee, user=user)
    tasks = Task.objects.filter(id=id).order_by('-id')
    return render(request, 'taskpage.html',{'tasks':tasks,'employee':employee})




@login_required(login_url='emplogin')
def home_room2(request,emp_name):
    emp_name = Task.objects.get(id=emp_name)
    print(emp_name)
    admin_user = User.objects.get(is_superuser=True)
    user = get_object_or_404(User, email=request.user.email)
    employee = get_object_or_404(Employee, user=user)

    context={
        'emp_name': emp_name,
        'admin_user': admin_user,
        'employee': employee
    }
    return render(request,'home_room2.html',context)

@login_required(login_url='emplogin')
def userprofile(request):
    user = get_object_or_404(User, email=request.user.email)
    employee = get_object_or_404(Employee, user=user)
    context={
        'employee': employee
    }
    return render(request,'userprofile.html',context)

