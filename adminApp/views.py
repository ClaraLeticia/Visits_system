from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from core.models import Department, CustomUser, Branch, Visits
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from collections import Counter

# Create your views here.
######################################## ADMINISTRADOR ########################################

# View para criação do dashboard com cards e informações das visitas
@login_required
@permission_required_or_403('core.admin_permission')
def admin_dashboard(request):
    ### Gráficos de visitas por setor  ####
    visits = Visits.objects.all().values_list('department__branch__name') # Busca todas as visitas e retorna os setores que foram realizadas as visitas
    visits_keys = [visit[0] for visit in visits] # Pega o nome dos setores
    visits_dict = dict(Counter(visits_keys)) # Conta a quantidade de visitas por setor
    visits_key = list(visits_dict.keys()) # Pega as chaves do dicionário
    visits_values = list(visits_dict.values()) # Pega os valores do dicionário
    

    ### Gráficos de visitas por departamento  ####
    visits_dp = Visits.objects.all().values_list('department__name') # Busca todas as visitas e retorna os departamentos que foram realizadas as visitas
    visits_dp_keys = [visit[0] for visit in visits_dp] # Pega o nome dos departamentos
    visits_dp_values = Counter(visits_dp_keys) # Conta a quantidade de visitas por departamento
    visits_dp_key = list(visits_dp_values.keys()) # Pega as chaves do dicionário
    visits_dp_values = list(visits_dp_values.values()) # Pega os valores do dicionário
    
   
    # Busca as visitas agendadas
    awaiting_visits = Visits.objects.filter(status='Agendada').values('visitor__name', 'status', 'date', 'id')
    # Busca as visitas confirmadas
    confirm_visits = Visits.objects.filter(status='Realizada').values('visitor__name', 'status', 'date', 'id')
    
    # Busca todas as unidades
    branches = Branch.objects.all().values('id', 'description', 'name')
    # Busca todos os setores
    departments = Department.objects.all().values('name', 'description', 'branch__name', 'id')
    # Busca todos os usuários, excluindo o usuário anônimo, que é criado pelo django toda vez que um usuário não logado interage com o sistema
    users = CustomUser.objects.exclude(username='AnonymousUser').values('email', 'phone', 'first_name', 'last_name', 'id')
    # Contexto para ser enviado ao template
    context = {
        'admin': request.user, # Envia o usuário logado
        'awaiting_visits': awaiting_visits.count(), # Envia a quantidade de visitas agendadas
        'confirmed_visits': confirm_visits.count(), # Envia a quantidade de visitas confirmadas
        'visits': visits.count(), # Envia a quantidade de visitas
        'visits_key': visits_key, # Envia os setores
        'visits_values': visits_values, #  Envia a quantidade de visitas por setor
        'visits_dp_key': visits_dp_key, # Envia os departamentos
        'visits_dp_values': visits_dp_values, # Envia a quantidade de visitas por departamento
        'branches': branches, # Envia as unidades
        'departments': departments, # Envia os setores
        'users': users # Envia os usuários
    }
    return render(request, 'admin/dashboard.html', context)


# Função para renderizar a tela de registro
def add_users(request):
    branches = Branch.objects.all().values('id', 'name')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # Cria o formulário com os dados do POST
        if form.is_valid(): # Se o formulário for válido
            user = form.save() # Salva o usuário
            return redirect('/administrador')
        else:
            # Se o formulário não for válido, renderiza a página de registro
            context = {'form': form, 'errors': form.errors, 'branches': branches}
            return render(request, 'admin/users/add_user.html', context)
    else:
        form = CustomUserCreationForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/users/add_user.html', context)
    
# Função para atualizar o usuário
@login_required
@permission_required_or_403('core.admin_permission')
def update_user(request, pk):
    branches = Branch.objects.all().values('id', 'name') # Busca todas as unidades para serem enviadas ao template
    user = get_object_or_404(CustomUser, id=pk) # Busca o usuário pelo id
    form = CustomUserChangeForm(instance=user) # Cria o formulário padrão com os dados do usuário
    if request.method == 'POST': # Se o método for POST
        user.set_password(request.POST.get('password')) # Atualiza a senha do usuário
        form = CustomUserChangeForm(request.POST, instance=user) # Cria o formulário com os dados do POST
        if form.is_valid(): # Se o formulário for válido
            form.save() # Salva o usuário
            return redirect('/administrador')
        else:
            # Se o formulário não for válido, renderiza a página de atualização de usuário
            context = {'form': form}
            return render(request, 'admin/users/update_user.html', context)
    else:
        return render(request, 'admin/users/update_user.html', {'form': form, 'branches': branches})

# Função para adicionar unidade
@login_required
@permission_required_or_403('core.admin_permission')
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST) # Cria o formulário com os dados do POST
        if form.is_valid():
            form.save() # Salva a unidade
            return redirect('/administrador')
        else:
            context = {'form': form}
            return render(request, 'admin/branches/add_branch.html', context)
    else:
        form = BranchForm()
        context = {'form': form}
        return render(request, 'admin/branches/add_branch.html', context)
    
# Função para atualizar a unidade
@login_required
@permission_required_or_403('core.admin_permission')
def update_branch(request, pk):
    branch = get_object_or_404(Branch, id=pk) # Busca a unidade pelo id
    if request.method == 'POST': # Se o método for POST
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save(branch=pk) # Salva a unidade
            return redirect('/administrador') # Redireciona para a página de administrador
        else:
            context = {'form': form}
            return render(request, 'admin/branches/update_branch.html', context)
    else:
        return render(request, 'admin/branches/update_branch.html', {'branch': branch})
    
# Função para adicionar setor    
@login_required
@permission_required_or_403('core.admin_permission')
def add_department(request):
    branches = Branch.objects.all().values('id', 'name') # Busca todas as unidades para serem enviadas ao template
    if request.method == 'POST':
        form = DepartmentForm(request.POST) # Cria o formulário com os dados do POST
        if form.is_valid(): # Se o formulário for válido
            form.save() # Salva o setor
            return redirect('/administrador')
        else:
            # Se o formulário não for válido, renderiza a página de adicionar setor
            context = {'form': form, 'branches': branches}
            return render(request, 'admin/departments/add_department.html', context)
    else:
        form = DepartmentForm()
        context = {'form': form, 'branches': branches}
        return render(request, 'admin/departments/add_department.html', context)
    
# Função para atualizar o setor 
@login_required
@permission_required_or_403('core.admin_permission')
def update_department(request, pk):
    department = get_object_or_404(Department, id=pk) # Busca o setor pelo id
    branches = Branch.objects.all() # Busca todas as unidades
    if request.method == 'POST': # Se o método for POST
        department.name = request.POST.get('name') # Atualiza o nome do setor
        department.branch_id = request.POST.get('branch') # Atualiza a unidade do setor
        department.description = request.POST.get('description') # Atualiza a descrição do setor
        department.save() # Salva o setor
        return redirect('/administrador')

    else:
        return render(request, 'admin/departments/update_department.html', {'department': department,'branches': branches})
