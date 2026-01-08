from django.shortcuts import redirect
from django.contrib import messages
# 

def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'USER':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Unauthorized access.')
        return redirect ('dashboard')
    return wrapper


def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'EMPLOYEE':
            return view_func(request, *args, **kwargs)
            messages.error(requestt, 'Unauthorized access.')
            return redirect('login')
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
       
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    return wrapper    
