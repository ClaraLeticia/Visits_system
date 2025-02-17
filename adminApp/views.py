from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from django.contrib import messages
from core.models import Department, CustomUser, Branch
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

# Create your views here.
######################################## ADMINISTRADOR ########################################

@login_required
@permission_required_or_403('core.admin_permission')
def admin_dashboard(request):
    visits = Visits.objects.all().values_list('department__branch__name', 'id')
    visits_dict = dict(visits)
    visits_key = list(visits_dict.keys())
    visits_values = list(visits_dict.values())

    visits_dp = dict(Visits.objects.all().values_list('department__name', 'id'))
    visits_dp_key = list(visits_dp.keys())
    visits_dp_values = list(visits_dp.values())

    awaiting_visits = Visits.objects.filter(status='Agendada').values('visitor__name', 'status', 'date', 'id')
    confirm_visits = Visits.objects.filter(status='Realizada').values('visitor__name', 'status', 'date', 'id')
    
    branches = Branch.objects.all().values('id', 'description', 'name')
    departments = Department.objects.all().values('name', 'description', 'branch__name', 'id')
    users = CustomUser.objects.exclude(username='AnonymousUser').values('email', 'phone', 'first_name', 'last_name', 'id')
    context = {
        'admin': request.user,
        'awaiting_visits': awaiting_visits.count(),
        'confirmed_visits': confirm_visits.count(),
        'visits': visits.count(),
        'visits_key': visits_key,
        'visits_values': visits_values,
        'visits_dp_key': visits_dp_key,
        'visits_dp_values': visits_dp_values,
        'branches': branches,
        'departments': departments,
        'users': users
    }
    return render(request, 'admin/dashboard.html', context)


# Função para renderizar a tela de registro
def add_users(request):
    branches = Branch.objects.all().values('id', 'name')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/administrador')
        else:
           
            context = {'form': form, 'errors': form.errors}
            return render(request, 'admin/users/add_user.html', context)
    else:
        form = CustomUserCreationForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/users/add_user.html', context)
    

@login_required
@permission_required_or_403('core.admin_permission')
def update_user(request, pk):
    branches = Branch.objects.all().values('id', 'name')
    user = get_object_or_404(CustomUser, id=pk)
    form = CustomUserChangeForm(instance=user)
    if request.method == 'POST':
        user.set_password(request.POST.get('password'))
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/administrador')
        else:
            print(form.errors)
            context = {'form': form}
            return render(request, 'admin/users/update_user.html', context)
    else:
        return render(request, 'admin/users/update_user.html', {'form': form, 'branches': branches})


@login_required
@permission_required_or_403('core.admin_permission')
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/administrador')
        else:
            context = {'form': form}
            return render(request, 'admin/branches/add_branch.html', context)
    else:
        form = BranchForm()
        context = {'form': form}
        return render(request, 'admin/branches/add_branch.html', context)
    

@login_required
@permission_required_or_403('core.admin_permission')
def update_branch(request, pk):
    branch = get_object_or_404(Branch, id=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save(branch=pk)
            return redirect('/administrador')
        else:
            context = {'form': form}
            return render(request, 'admin/branches/update_branch.html', context)
    else:
        return render(request, 'admin/branches/update_branch.html', {'branch': branch})
    
@login_required
@permission_required_or_403('core.admin_permission')
def add_department(request):
    branches = Branch.objects.all().values('id', 'name')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/administrador')
        else:
            context = {'form': form, 'branches': branches}
            return render(request, 'admin/departments/add_department.html', context)
    else:
        form = DepartmentForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/departments/add_department.html', context)
    

    
@login_required
@permission_required_or_403('core.admin_permission')
def update_department(request, pk):
    department = get_object_or_404(Department, id=pk)
    branches = Branch.objects.all()
    form = DepartmentForm(instance=department)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.branch_id = request.POST.get('branch')
        department.description = request.POST.get('description')
        department.save()
        return redirect('/administrador')

    else:
        return render(request, 'admin/departments/update_department.html', {'department': department,'branches': branches})
