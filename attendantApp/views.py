from django.shortcuts import render, redirect
from core.forms import *
from core.models import Visitor, Visits
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

######################################## ATENDETENTE ########################################
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
            return redirect(f'/atendente/add-visit/?cpf={cpf}')
        else:
            Visitor.objects.create(cpf=cpf, name=name, rg=rg, phone=phone, photo=photo)
            return redirect(f'/atendente/add-visit/?cpf={cpf}')   
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


## Cadastro de visitas
#@login_required
#@permission_required_or_403('core.attendant_permission')
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

