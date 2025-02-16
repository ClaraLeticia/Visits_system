from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from core.forms import *
from django.contrib import messages
from .models import Visitor, Visits
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required


        
# Função para retornar os setores de uma unidade em específico
#@login_required
#@permission_required_or_403('core.admin_permission')
def get_departments(request):
    branch_id = request.GET.get('branch_id')
    departments = Department.objects.filter(branch_id=branch_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

#@login_required
#@permission_required_or_403('core.admin_permission')
def get_func_user(request):
    department_id = request.GET.get('department_id')
    users = CustomUser.objects.filter(department_id=department_id, funcionario = True).values('id', 'username')
    return JsonResponse({'users': list(users)})

######################################## ATENDETENTE ########################################
## Cadastro de visitas
#@login_required
#@permission_required_or_403('core.attendant_permission')
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
#@login_required
#@permission_required_or_403('core.attendant_permission')
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
    
#@login_required
#@permission_required_or_403('core.attendant_permission')
def add_visitor(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        name = request.POST.get('name')
        rg = request.POST.get('rg')
        phone = request.POST.get('phone')
        photo = f"/profile_pictures/{request.FILES.get('photo')}"
        
        if Visitor.objects.filter(cpf=cpf).exists():
            visits = Visitor.objects.filter(cpf=cpf)
            visits.update(name=name, rg=rg, phone=phone, photo=photo)
            return redirect(f'/add-visit/?cpf={cpf}')
        else:
            Visitor.objects.create(cpf=cpf, name=name, rg=rg, phone=phone, photo=photo)
            return redirect(f'/add-visit/?cpf={cpf}')   
    else:
        form = VisitorForm()
        context = {'form': form}
        return render(request, 'attendant/add_visitor.html', context)

    
 # Função para retornar a lista de visitantes
#@login_required
#@permission_required_or_403('core.attendant_permission')
def get_visitors_by_cpf(request):
    cpf = request.GET.get('cpf')
    visitor = Visitor.objects.filter(cpf=cpf)
    if visitor:
        visitor = visitor.first()
        return JsonResponse({
            'name': visitor.name,
            'rg': visitor.rg,
            'phone': visitor.phone,
            'photo': visitor.photo.url if visitor.photo else None       
        })
    else:
        return JsonResponse({'error': 'Visitante não encontrado'})    
    
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
    
def logoutView(request):
    logout(request)
    return redirect('/login')