from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core.forms import CustomUserCreationForm, VisitorForm
from django.contrib import messages
from .models import Department, Visitor
from django.http import JsonResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required

# Função para renderizar a tela de registro
def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login')
        else:
            context = {'form': form}
            return render(request, 'registration/register.html', context)
    else:
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

# Função para retornar os setores de uma unidade em específico
def get_departments(request):
    branch_id = request.GET.get('branch_id')
    departments = Department.objects.filter(branch_id=branch_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

# Função para retornar a lista de visitantes
@login_required # Decorator para verificar se o usuário está logado
@permission_required_or_403('core.view_visitor') # Decorator para verificar se o usuário tem permissão para visualizar visitantes
def get_visitors(request):
    context = {'visitors':Visitor.objects.all()}
    return render(request, 'visitor/list_visitors.html', context)

@permission_required_or_403('core.add_visitor') # Decorator para verificar se o usuário tem permissão para adicionar visitantes
def add_visitor(request):
    if request.method == 'POST':
        form = VisitorForm()
        if form.is_valid():
            visitor = form.save()
        return redirect('/get-visitors')
    else:
        context = VisitorForm()
        form = {'form': context}
        return render(request, 'visitor/add_visitor.html', form)

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
            return redirect('/get-visitors')
        else:
        # Se o usuário não for válido, uma mensagem de erro é exibida
            messages.info(request, 'Usuário ou senha incorretos')
            return render(request, 'registration/login.html')

    else:
        # Se o método for diferente de POST, a página de login é renderizada
        return render(request, 'registration/login.html')