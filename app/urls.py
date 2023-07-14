from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    # path('empdashboard/',views.empdashboard,name='empdashboard'),
    path('emplogin/',views.emplogin,name='emplogin'),
    path('emplogout/',views.emplogout,name='emplogout'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('mytasks/',views.mytasks,name='mytasks'),
    path('taskpage/<int:id>',views.taskpage,name='taskpage'),
    path('home_room2/<str:emp_name>',views.home_room2,name='home_room2'),
]
