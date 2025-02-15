from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from core.forms import *
from django.contrib import messages
from .models import Department, Visitor, CustomUser, Visits, Branch
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView




######################################## ATENDETENTE ########################################
## Cadastro de visitas
#@login_required
#@permission_required_or_403('core.add_visits')
def attendant_dashboard(request):
    
    visits = Visits.objects.filter(department__branch=request.user.branch).order_by('-date').values('visitor__name', 'status', 'date', 'id')
    confimed_visits = visits.filter(status='Realizada').values('visitor__name', 'status', 'date')
    awaiting_visits = visits.filter(status='Agendada').values('visitor__name', 'status', 'date')

    context = {
        'attendant': request.user, 
        'visits': visits,
        'awaiting_visits': awaiting_visits,
        'confirmed_visits': confimed_visits,
        'visits_count': visits.count(),
        'awaiting_count': awaiting_visits.count(),
        'confirmed_count': confimed_visits.count(),

    }
    return render(request, 'attendant/dashboard.html', context)

def add_visit(request):
    if request.method == 'POST':
        cpf = request.GET.get('cpf')
        visitor = Visitor.objects.get(cpf=cpf)
        form = VisitsForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.visitor = visitor
            visit = form.save()
            return redirect('/atendente')
        else:
            context = {'form': form}
            return render(request, 'attendant/add_visit.html', context)
    else:
        form = VisitsForm()
        context = {'form': form}
        return render(request, 'attendant/add_visit.html', context)
    
# Cadastro de visitante    
#@permission_required_or_403('core.add_visitor') # Decorator para verificar se o usuário tem permissão para adicionar visitantes
def add_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save()
            return redirect(f'/add-visit/?cpf={visitor.cpf}')
        else:
            
            context = {'form': form}
            return render(request, 'attendant/add_visitor.html', context)

    else:
        context = VisitorForm()
        form = {'form': context}
        return render(request, 'attendant/add_visitor.html', form)
    
 # Função para retornar a lista de visitantes
#@login_required # Decorator para verificar se o usuário está logado
#@permission_required_or_403('core.view_visitor') # Decorator para verificar se o usuário tem permissão para visualizar visitantes
def get_visitors_by_cpf(request):
    cpf = request.GET.get('cpf')
    visitor = Visitor.objects.filter(cpf=cpf)
    if visitor:
        visitor = visitor.first()
        return JsonResponse({
            'name': visitor.name,
            'rg': visitor.rg,
            'phone': visitor.phone
            
        })
    else:
        return JsonResponse({'error': 'Visitante não encontrado'})

######################################## Funcionario ########################################
#@login_required
#@permission_required_or_403('core.change_confirm_visits_employee')
def get_visits_by_func(request):
    awaiting_visits = Visits.objects.filter(user=request.user, status='Agendada').values('visitor__name', 'status', 'date', 'id')
    confirm_visits = Visits.objects.filter(user=request.user, status='Realizada').values('visitor__name', 'status', 'date', 'id')

    context = {
        'employee': request.user,
        'awaiting_visits': awaiting_visits,
        'confirmed_visits': confirm_visits,
        'awaiting_count': awaiting_visits.count(),
        'confirmed_count': confirm_visits.count(),
    }


    return render(request, 'employee/get_visits.html', context)

#@login_required
#@permission_required_or_403('core.change_confirm_visits_employee')
def confirm_visit(request):
    visit_id = request.GET.get('visit_id')
    visit = Visits.objects.get(id=visit_id)
    visit.status = 'Realizada'
    visit.save()
    return redirect('/func/get-visits')
    
    

######################################## ADMINISTRADOR ########################################
# Função para renderizar a tela de registro
def add_users(request):
    branches = Branch.objects.all().values('id', 'name')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login')
        else:
            print(form.errors)
            context = {'form': form, 'errors': form.errors}
            return render(request, 'admin/users/add_user.html', context)
    else:
        form = CustomUserCreationForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/users/add_user.html', context)

# Função para retornar os setores de uma unidade em específico
def get_departments(request):
    branch_id = request.GET.get('branch_id')
    departments = Department.objects.filter(branch_id=branch_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

def get_func_user(request):
    department_id = request.GET.get('department_id')
    users = CustomUser.objects.filter(department_id=department_id, funcionario = True).values('id', 'username')
    return JsonResponse({'users': list(users)})


def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add-branch')
        else:
            print(form.errors)
            context = {'form': form}
            return render(request, 'admin/branches/add_branch.html', context)
    else:
        form = BranchForm()
        context = {'form': form}
        return render(request, 'admin/branches/add_branch.html', context)
    
def add_department(request):
    branches = Branch.objects.all().values('id', 'name')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add-department')
        else:
            context = {'form': form, 'branches': branches}
            return render(request, 'admin/departments/add_department.html', context)
    else:
        form = DepartmentForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/departments/add_department.html', context)

### Preparando crud branch ###
def list_branches(request):
    branchs = Branch.objects.all()
    return render(request, 'admin/branches/list_branches.html', {'branches': branchs})

def update_branch(request, pk):
    branch = get_object_or_404(Branch, id=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save(branch=pk)
            return redirect('/list-branches')
        else:
            context = {'form': form}
            return render(request, 'admin/branches/update_branch.html', context)
    else:
        return render(request, 'admin/branches/update_branch.html', {'branch': branch})
    


#### prerando crud para setores ###
def list_departments(request):
    departments = Department.objects.all()
    return render(request, 'admin/departments/list_departments.html', {'departments': departments})
    

def update_department(request, pk):
    department = get_object_or_404(Department, id=pk)
    branches = Branch.objects.all()
    form = DepartmentForm(instance=department)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.branch_id = request.POST.get('branch')
        department.description = request.POST.get('description')
        department.save()
        return redirect('/list-departments')

    else:
        return render(request, 'admin/departments/update_department.html', {'department': department,'branches': branches})
    

### Crud usuários ###

def list_users(request):
    users = CustomUser.objects.exclude(username='AnonymousUser')
    return render(request, 'admin/users/list_users.html', {'users': users})

def update_user(request, pk):
    branches = Branch.objects.all().values('id', 'name')
    user = get_object_or_404(CustomUser, id=pk)
    form = CustomUserChangeForm(instance=user)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/list-users')
        else:
            context = {'form': form}
            return render(request, 'admin/users/update_user.html', context)
    else:
        return render(request, 'admin/users/update_user.html', {'form': form, 'branches': branches})
    
######################################## USUÁRIOS ########################################

# Função para renderizar a tela de login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username') # Pega o valor do campo username do formulário
        password = request.POST.get('password') # Pega o valor do campo password do formulário
        # O método autheticate verifica se o usuário e senha são válidos
        user = authenticate(request, username=username, password=password) 
        # Se o usuário for válido, o método login é chamado e o usuário é logado no sistema
        if user is not None:
            login(request, user)
            return redirect('/add-visitors')
        else:
        # Se o usuário não for válido, uma mensagem de erro é exibida
            messages.info(request, 'Usuário ou senha incorretos')
            return render(request, 'registration/login.html')

    else:
        # Se o método for diferente de POST, a página de login é renderizada
        return render(request, 'registration/login.html')
    