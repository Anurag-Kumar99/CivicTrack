from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Complaint, Department, User, UserProfile
from .forms import ComplaintForm
from .forms import ResolveComplaintForm
# from django.shortcuts import get_object_or_404
from .decorators import user_required, employee_required, admin_required
from django.db.models import Case, When, IntegerField

# Create your views here.
def home(request):
    return redirect('register')  

def user_register(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        city = request.POST.get('city')
        area = request.POST.get('area')
        pincode = request.POST.get('pincode')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            role='USER'
        )    

        UserProfile.objects.create(
            user =user,
            full_name=full_name,
            phone=phone,
            state=state,
            city=city,
            area=area,
            pincode=pincode
        )
        

        
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 🔐 BACKEND VERIFICATION
            if login_type == 'user' and user.role == 'USER':
                login(request, user)
                return redirect('user_dashboard')

            elif login_type == 'employee' and user.role == 'EMPLOYEE':
                login(request, user)
                return redirect('employee_dashboard')

            elif login_type == 'admin' and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')

            else:
                messages.error(request, "Selected portal does not match your account role.")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

@login_required
def dashboard_redirect(request):
    user = request.user

    if user.role == 'ADMIN':
        return redirect('admin_dashboard')

    elif user.role == 'EMPLOYEE':
        return redirect('employee_dashboard')
    else:
        return redirect('user_dashboard')

@login_required
@user_required
def user_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/dashboard.html', {'complaints': complaints})
@login_required
@employee_required
def employee_dashboard(request):
    priority_order = Case(
        When(priority='HIGH', then=1),
        When(priority='MEDIUM', then=2),
        When(priority='LOW', then=3),
        output_field=IntegerField(),
    )
    
    
    complaints = Complaint.objects.filter(
        assigned_employee=request.user
        ).annotate(
        priority_rank=priority_order
    ).order_by('priority_rank', '-created_at')
        
    return render(request, 'employee/dashboard.html', {'complaints': complaints})


@login_required
@admin_required
def admin_dashboard(request):
    status_filter = request.GET.get('status')  
    category_filter = request.GET.get('category')

    proority_order = Case(
        When(priority='HIGH', then=1),
        When(priority='MEDIUM', then=2),
        When(priority='LOW', then=3),
        output_field=IntegerField(),
    )
    complaints = Complaint.objects.annotate(
        priority_rank=proority_order
    )

    if status_filter:
        complaints = complaints.filter(status=status_filter)

    if category_filter:
        complaints = complaints.filter(category=category_filter)

    complaints = complaints.order_by('priority_rank', '-created_at')

    # if status_filter == 'PENDING':
    #     complaints = Complaint.objects.filter(status='PENDING')
    # elif status_filter == 'RESOLVED':
    #     complaints = Complaint.objects.filter(status='RESOLVED')
    # else:
    #     complaints = Complaint.objects.all() 


    # complaints = complaints.order_by('-created_at')

    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status='PENDING').count()
    resolved = Complaint.objects.filter(status='RESOLVED').count()

    # complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/dashboard.html', {
        'total': total,
        'pending': pending,
        'resolved': resolved,
        'complaints': complaints,
        'category_filter': category_filter,
        # 'status_filter': status_filter

    })


def user_logout(request):
    logout(request)
    return redirect('login') 


@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            complaint = form.save(commit=False)
            complaint.user = request.user
            # Auto-assign employee based on department
            employee = auto_assign_employee(complaint)
            if employee:
                complaint.assigned_employee = employee
                complaint.status = 'PENDING'
            
            complaint.save()
            return redirect('user_dashboard')
           
    else:
        form = ComplaintForm()
    return render(request, 'user/create_complaint.html', {'form': form})

@login_required
def accept_complaint(request, id):
    complaint = Complaint.objects.get(id=id, assigned_employee=request.user)
    complaint.status = 'ACCEPTED'
    complaint.save()
    return redirect('employee_dashboard')



@login_required
def resolve_complaint(request, id):
    complaint = Complaint.objects.get(id=id, assigned_employee=request.user)

    if request.method == 'POST':
        form = ResolveComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            resolved = form.save(commit=False)
            resolved.status = 'RESOLVED'
            resolved.save()
            return redirect('employee_dashboard')

    else:
        form = ResolveComplaintForm(instance=complaint)

    return render(request, 'employee/resolve.html', {'form': form, 'complaint': complaint})
                

@login_required
def assign_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    employess = User.objects.filter(role='EMPLOYEE')
    if request.method == 'POST':
        employee_id = request.POST.get('employee')

        if not employee_id:
            messages.error(request, "Please select an employee to assign the complaint.")
            return redirect('assign_complaint', id=id)


        employee = get_object_or_404(User, id=employee_id, role='EMPLOYEE')
        complaint.assigned_employee = employee
        complaint.status = 'PENDING'
        complaint.save()
        messages.success(request, "Complaint assigned successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin_panel/assign.html', {
        'complaint': complaint,
         'employees': employess
         })    

User = get_user_model()
def auto_assign_employee(complaint):
    # Get all employees in the same department
    employees = User.objects.filter(
        role='EMPLOYEE',
        department=complaint.department
    )
    if employees.exists():
        # Assign the first available employee
        return employees.first()
        # employee = employees.first()
        # complaint.assigned_employee = employee
        # complaint.status = 'PENDING'
        # complaint.save()
    return None    