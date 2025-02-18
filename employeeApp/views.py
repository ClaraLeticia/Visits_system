from django.shortcuts import render, redirect
from core.models import Visits
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

# Create your views here.

######################################## Funcionario ########################################

# View para criação do dashboard com cards e informações das visitas
@login_required
@permission_required_or_403('core.employee_permission')
def employee_dashboard(request):
    # Busca as visitas agendadas para o funcionário
    awaiting_visits = Visits.objects.filter(user=request.user, status='Agendada').values('visitor__name', 'status', 'date', 'id', 'visitor__photo')
    # Busca as visitas confirmadas para o funcionário
    confirm_visits = Visits.objects.filter(user=request.user, status='Realizada').values('visitor__name', 'status', 'date', 'id')

    # Contexto para ser enviado ao template
    context = {
        'employee': request.user, # Envia o usuário logado
        'awaiting_visits': awaiting_visits, # Envia as visitas agendadas
        'confirmed_visits': confirm_visits, # Envia as visitas confirmadas
        'awaiting_count': awaiting_visits.count(), # Envia a quantidade de visitas agendadas
        'confirmed_count': confirm_visits.count(), # Envia a quantidade de visitas confirmadas
    }


    return render(request, 'employee/dashboard.html', context)

# View para confirmar a visita
@login_required
@permission_required_or_403('core.employee_permission')
def confirm_visit(request,pk):
    visit_id = pk  # Pega o id da visita
    visit = Visits.objects.get(id=visit_id) # Busca a visita pelo id
    visit.status = 'Realizada' # Atualiza o status da visita
    visit.save() # Salva a visita
    return redirect('/funcionario')
    
