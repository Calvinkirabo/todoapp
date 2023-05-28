from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name= 'home'),
    path('', auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    path('update_list/task<str:pk>/', views.updateList, name="update_list"),
    path('delete/task<str:pk>/', views.deleteTask, name="delete"),
    path('add_task/', views.add_task, name='add_task'),
    path('task_list/', views.task_list, name='task_list'),
    
]