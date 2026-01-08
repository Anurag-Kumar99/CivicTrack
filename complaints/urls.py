from django.urls import path
from . import views

urlpatterns = [

   path('', views.home, name='home'),

path('register/', views.user_register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),

path('dashboard/', views.dashboard_redirect, name='dashboard'),

path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

path('dashboard/admin/assign/<int:id>/', views.assign_complaint, name='assign_complaint'),

path('user/complaint/new/', views.create_complaint, name='create_complaint'),

path('employee/accept/<int:id>/', views.accept_complaint, name='accept_complaint'),
path('employee/resolve/<int:id>/', views.resolve_complaint, name='resolve_complaint'),
]
