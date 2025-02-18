from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from core.forms import *
from core.models import Visitor, Visits
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

######################################## ATENDETENTE ########################################

# View para criação do dashboard com cards e informações das visitas
@login_required
@permission_required_or_403('core.attendant_permission')
def attendant_dashboard(request):
    # Busca as visitas que estão relacionadas com as unidades do atendente
    visits = Visits.objects.filter(department__branch=request.user.branch).order_by('-date').values('visitor__name', 'status', 'date', 'id')
    # Busca as visitas realizadas da unidade do atendente
    confimed_visits = visits.filter(status='Realizada').values('visitor__name', 'status', 'date')
    # Busca as visitas agendadas da unidade do atendente
    awaiting_visits = visits.filter(status='Agendada').values('visitor__name', 'status', 'date')

    # Contexto para ser enviado ao template
    context = {
        'attendant': request.user,  # envia o usuário logado
        'visits': visits, # envia as visitas
        'awaiting_visits': awaiting_visits, # envia as visitas agendadas
        'confirmed_visits': confimed_visits, # envia as visitas confirmadas
        'visits_count': visits.count(), # envia a quantidade de visitas
        'awaiting_count': awaiting_visits.count(), # envia a quantidade de visitas agendadas
        'confirmed_count': confimed_visits.count(), # envia a quantidade de visitas confirmadas

    }
    return render(request, 'attendant/dashboard.html', context)

# View para adicionar visitantes
@login_required
@permission_required_or_403('core.attendant_permission')
def add_visitor(request):
    if request.method == 'POST': # Se o método for POST
        form = VisitorForm(request.POST, request.FILES) # Cria o formulário com os dados do POST
        if form.is_valid(): # Se o formulário for válido
            visitor = form.save() # Salva o visitante
            cpf = visitor.cpf # Pega o CPF do visitante
            return redirect(f'/atendente/add-visit/?cpf={cpf}') # Redireciona para a página de adicionar visitas
        else:
            # Se o formulário não for válido, renderiza a página de adicionar visitantes
            context = {'form': form}
            return render(request, 'attendant/add_visitor.html', context)
    else:
        # Se o método for diferente de POST, renderiza a página de adicionar visitantes
        form = VisitorForm()
        context = {'form': form}
        return render(request, 'attendant/add_visitor.html', context)

    
 # Função para retornar o visitante pelo cpf
@login_required
@permission_required_or_403('core.attendant_permission')
def get_visitors_by_cpf(request):
    cpf = request.GET.get('cpf') # Pega o cpf do visitante
    visitor = Visitor.objects.filter(cpf=cpf) # Busca o visitante pelo cpf
    if visitor: 
        visitor = visitor.first() # Pega o primeiro visitante encontrado
        # Retorna os dados do visitante como uma resposta json
        return JsonResponse({
            'name': visitor.name, # Retorna o nome do visitante
            'rg': visitor.rg, # Retorna o rg do visitante
            'phone': visitor.phone, # Retorna o telefone do visitante
            'photo': visitor.photo.url if visitor.photo else None  # Retorna a foto do visitante
        })
    else:
        return JsonResponse({'error': 'Visitante não encontrado'})  


## Cadastro de visitas
@login_required
@permission_required_or_403('core.attendant_permission')
def add_visit(request):
    if request.method == 'POST':
        cpf = request.GET.get('cpf') # Pega o cpf do visitante
        visitor = Visitor.objects.get(cpf=cpf) # Busca o visitante pelo cpf
        form = VisitsForm(request.POST) # Cria o formulário com os dados do POST
        if form.is_valid(): # Se o formulário for válido
            visit = form.save(commit=False) # Salva a visita, mas sem salvar no banco de dados
            visit.visitor = visitor # Adiciona o visitante à visita
            visit = form.save() # Salva a visita
            return redirect('/atendente')
        else:
            context = {'form': form}
            return render(request, 'attendant/add_visit.html', context)
    else:
        form = VisitsForm()
        context = {'form': form}
        return render(request, 'attendant/add_visit.html', context)
      

        
# Função para retornar os setores de uma unidade em específico
@login_required
def get_departments(request):
    branch_id = request.GET.get('branch_id') # Pega o id da unidade
    departments = Department.objects.filter(branch_id=branch_id).values('id', 'name') # Busca os setores da unidade
    return JsonResponse({'departments': list(departments)}) # Retorna os setores como uma resposta json

# Função para retornar os funcionários de um setor em específico
@login_required
@permission_required_or_403('core.attendant_permission')
def get_func_user(request):
    department_id = request.GET.get('department_id') # Pega o id do setor
    users = CustomUser.objects.filter(department_id=department_id, funcionario = True).values('id', 'username') # Busca os funcionários do setor
    return JsonResponse({'users': list(users)}) # Retorna os funcionários como uma resposta json

