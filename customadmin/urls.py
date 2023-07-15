from django.contrib import admin
from django.urls import include, path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', admin_login,name='admin_login'),
    path('admin_logout/', admin_logout,name='admin_logout'),
    # path('dashboard/', dashboard,name='dashboard'),
    path('admin_profile/', admin_profile,name='admin_profile'),
    path('add_task/',add_task,name='add_task'),
    path('task_history/',task_history,name='task_history'),
    path('add_employee/',add_employee,name='add_employee'),
    path('update_employee/<int:id>/',update_employee,name='update_employee'),
    path('delete_employee/<int:id>/',delete_employee,name='delete_employee'),
    path('update_status/<int:id>',update_status,name='update_status'),
    path('search_employee/',search_employee,name='search_employee'),
    path('search_tasks/',search_tasks,name='search_tasks'),
    path('home_room/<str:emp_name>', home_room,name='home_room'),
    path('home_room/<str:room>/',room, name='room'),
    path('checkview',checkview, name='checkview'),
    path('send', send, name='send'),
    path('getMessages/<str:room>/',getMessages, name='getMessages'),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
