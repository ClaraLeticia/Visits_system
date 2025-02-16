from django.shortcuts import render, redirect
from core.models import Visits
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

# Create your views here.

######################################## Funcionario ########################################
#@login_required
#@permission_required_or_403('core.employee_permission')
def employee_dashboard(request):
    awaiting_visits = Visits.objects.filter(user=request.user, status='Agendada').values('visitor__name', 'status', 'date', 'id', 'visitor__photo')
   
    confirm_visits = Visits.objects.filter(user=request.user, status='Realizada').values('visitor__name', 'status', 'date', 'id')

    context = {
        'employee': request.user,
        'awaiting_visits': awaiting_visits,
        'confirmed_visits': confirm_visits,
        'awaiting_count': awaiting_visits.count(),
        'confirmed_count': confirm_visits.count(),
    }


    return render(request, 'employee/dashboard.html', context)

#@login_required
#@permission_required_or_403('core.employee_permission')
def confirm_visit(pk):
    visit_id = pk
    visit = Visits.objects.get(id=visit_id)
    visit.status = 'Realizada'
    visit.save()
    return redirect('/funcionario')
    
