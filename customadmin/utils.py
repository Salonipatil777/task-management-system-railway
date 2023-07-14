from django.core.mail import send_mail
from django.conf import settings

from customadmin.models import Employee


def send_mail_to_employee():
    empdetails = Employee.objects.all()
    subject ="Hiiiiiiii"
    message =[empdetails]
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["salonipatil7777@gmail.com"]
    send_mail(subject,message,from_email,recipient_list)