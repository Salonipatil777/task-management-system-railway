from email import message
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from customadmin.models import *
from customadmin.models import Employee
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



# Create your views here.
# Create your views here.
def admin_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Check if the user with the provided username exists
            user_query = User.objects.filter(username=username)
            if not user_query.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Authenticate the user with the provided username and password
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None and user_obj.is_superuser:
                login(request, user_obj)
                messages.success(request, 'Admin login successful')
                return redirect('/admin/dashboard/')
            
            messages.info(request, 'Invalid password')
            return redirect('/')

        # For GET requests, simply render the login page
        return render(request, 'login.html')

    except Exception as e:
        print(e)
        # You might want to handle the exception and return an appropriate response here

    # Make sure to return a response in all cases to avoid the "None" error
    return render(request, 'login.html')

        
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect('admin_login')

@login_required(login_url='admin_login')
def dashboard(request):
    employee = Employee.objects.all().order_by('id')[0:5]
    context = {
        'employee': employee,
    }   

    return render(request,'dashboard.html',context)

@login_required(login_url='admin_login')
def add_task(request):
    emp = Employee.objects.all().order_by('id')[0:5]
    if request.method == 'POST':
        assigned_to = request.POST.get('assigned_to')
        employee_name = request.POST.get('employee_name')
        given_task = request.POST.get('given_task')
        task_description = request.POST.get('task_description')
        created_date = request.POST.get('created_date')
        target_date = request.POST.get('target_date')
        status = request.POST.get('status')
        image = request.FILES.get('image')



        user = get_object_or_404(User, email=assigned_to)
        employee = get_object_or_404(Employee, user=user)
        task = Task.objects.create(
        assigned_to=employee,
        given_task=given_task,
        task_description=task_description,
        created_date=created_date,
        target_date=target_date,
        status=status,
        employee_name=employee_name,
        image=image,
        )
        task.save()
        messages.success(request, 'Task created successfully')
        return redirect('task_history')   

    context = {
        'emp': emp,
    }    
       

    return render(request,'add_task.html',context)

@login_required(login_url='admin_login')
def task_history(request):
    tasks = Task.objects.all().order_by('-id')
    assigned_tasks = Task.objects.filter(status='Assign')
    completed_tasks = Task.objects.filter(status='Complete')
    pending_tasks = Task.objects.filter(status='Pending')
    cancel_tasks = Task.objects.filter(status='Cancel')
    delay_tasks = Task.objects.filter(status='Delay')
    reassign_tasks = Task.objects.filter(status='Reassign')
    # tasks = tasks.reverse()
    page = Paginator(tasks,3)
    page_number = request.GET.get('page')
    page=page.get_page(page_number)


    context = {
        'page': page,
        'assigned_tasks':assigned_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks':pending_tasks,
        'cancel_tasks':cancel_tasks,
        'delay_tasks':delay_tasks,
        'reassign_tasks':reassign_tasks,
    }    
       

    return render(request,'task_history.html',context)

@login_required(login_url='admin_login')
def add_employee(request):
    if request.method == 'POST':
        emp_name = request.POST.get('emp_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        date_of_join = request.POST.get('date_of_join')
        date_of_birth = request.POST.get('date_of_birth')
        post = request.POST.get('post')
        address = request.POST.get('address')
        blood_group = request.POST.get('blood_group')
        image = request.FILES.get('image')
        
        ctx = {
           'email' : email,
           'password' : password
        }
        message = render_to_string('mail.html', ctx)
        
        send_mail(
        'User Info',
        message,
        settings.EMAIL_HOST_USER,
        [email], 
        fail_silently=False, html_message=message)


        #check email
        if Employee.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('add_employee')
        
        # employee.set_password(password)
        user = User.objects.create_user(email,email,password)
        user = User.objects.get(email=email)
        employee = Employee.objects.create(
            user=user,
            emp_name=emp_name,
            email=email,
            password=password,
            mobile=mobile,
            date_of_join=date_of_join,
            date_of_birth=date_of_birth,
            post=post,
            address=address,
            image=image,
            blood_group=blood_group,)
        employee.save()
        user.save()
        return redirect('dashboard') 



    return render(request,'add_employee.html')

@login_required(login_url='admin_login')
def search_employee(request):
    query = request.GET.get('query')
    if len(query)>50:
        employee = Employee.objects.none()
    else:
        employeeName = Employee.objects.filter(emp_name__icontains=query)
        employeeEmail = Employee.objects.filter(email__icontains=query)
        employee = employeeName.union(employeeEmail)
    if employee.count()==0:
        messages.warning(request,'No Search Results Found. Please refind your search')
    params = {'employee':employee,'query':query}
    return render(request,'search.html',params)

@login_required(login_url='admin_login')
def home_room(request ,emp_name):
    emp_name = Task.objects.get(id=emp_name)
    context={
        'emp_name': emp_name
    }
    return render(request,'home_room.html',context)

@login_required(login_url='admin_login')
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    employee = get_object_or_404(User, email=request.user.email)
    emp = Employee.objects.filter(email=request.user.email)

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'employee': employee,
        'emp':emp
    })

@login_required(login_url='admin_login')
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('home_room/' +room+ '/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('home_room/' +room+ '/?username='+username)

@login_required(login_url='admin_login')
def send(request):
    message = request.POST.get('message')
    username = request.POST.get('username')
    room_id = request.POST.get('room_id')

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required(login_url='admin_login')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

@login_required(login_url='admin_login')
def delete_employee(request,id):
    employee = Employee.objects.get(id=id)
    user = get_object_or_404(User, email=employee.email)
    employee.delete()
    user.delete()
    messages.success(request, "Employee deleted successfully")
    return render(request, 'dashboard.html', {'id': id})

@login_required(login_url='admin_login')
def update_employee(request,id):
    employee = Employee.objects.get(id=id)
    user = get_object_or_404(User, email=employee.email)
    if request.method == 'POST':
        emp_name = request.POST.get('emp_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        date_of_birth = request.POST.get('date_of_birth')
        date_of_join = request.POST.get('date_of_join')
        post = request.POST.get('post')
        address = request.POST.get('address')
        blood_group = request.POST.get('blood_group')
        image = request.FILES.get('image')


        ctx = {
           'email' : email,
           'password' : password
        }
        message = render_to_string('mail.html', ctx)
        
        send_mail(
        'Updated User Info',
        message,
        settings.EMAIL_HOST_USER,
        [email], 
        fail_silently=False, html_message=message)


        # employee.set_password(password)
        user = User(username=email,
                    email=email,
                    password=password
                    )
        user = User.objects.get(email=email)
        employee = Employee(
            id=id,
            user=user,
            emp_name=emp_name,
            email=email,
            password=password,
            mobile=mobile,
            post=post,
            address=address,
            image=image,
            blood_group=blood_group,
            date_of_birth = date_of_birth,
            date_of_join = date_of_join,)
        employee.save()
        user.save()
        messages.success(request, "Employee update successfully")
        return redirect('dashboard') 
    
    return render(request, 'update_employee.html', {'employee': employee,'user': user})


@login_required(login_url='admin_login')
def update_status(request,id):
    tsk = Task.objects.get(id=id)
    if request.method == 'POST':
        status=request.POST.get('status')

        task = Task(
            id=id,
            status=status,
            given_task=tsk.given_task,
            task_description=tsk.task_description,
            created_date=tsk.created_date,
            assigned_to=tsk.assigned_to,
            employee_name=tsk.employee_name,
            target_date=tsk.target_date
            )
        
        task.save()
        messages.success(request, "Status update successfully")
        return redirect('task_history') 
    
    return render(request, 'task_history.html',{'tsk':tsk,'selected_status': tsk.status,})
    

@login_required(login_url='admin_login')
def search_tasks(request):
    assigned_tasks = Task.objects.filter(status='Assign')
    completed_tasks = Task.objects.filter(status='Complete')
    pending_tasks = Task.objects.filter(status='Pending')
    cancel_tasks = Task.objects.filter(status='Cancel')
    delay_tasks = Task.objects.filter(status='Delay')
    reassign_tasks = Task.objects.filter(status='Reassign')


       
    query = request.GET.get('query')
    if len(query)>50:
        tsk = Task.objects.none()
    else:
        tsk = Task.objects.filter(status__icontains=query)
    if tsk.count()==0:
        messages.warning(request,'No Search Results Found. Please refind your search')
    params = {'tsk':tsk,'query':query}
    context = {
        'assigned_tasks':assigned_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks':pending_tasks,
        'cancel_tasks':cancel_tasks,
        'delay_tasks':delay_tasks,
        'reassign_tasks':reassign_tasks,
        **params  
    } 
    return render(request,'searchtsk.html',context)


@login_required(login_url='admin_login')
def admin_profile(request):
    return render(request,'admin_profile.html')
