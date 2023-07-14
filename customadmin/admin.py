from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Status)

