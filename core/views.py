from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from core.forms import CustomUserCreationForm
from django.contrib import messages
from .models import Department
from django.http import JsonResponse


# Função para renderizar a tela de registro
def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login')
        else:
            print('Formulário inválido')
            print(form.errors)
            context = {'form': form}
            return render(request, 'registration/register.html', context)
    else:
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)
    
def get_departments(request):
    branch_id = request.GET.get('branch_id')
    departments = Department.objects.filter(branch_id=branch_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

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
            return redirect('/admin')
        else:
        # Se o usuário não for válido, uma mensagem de erro é exibida
            messages.info(request, 'Usuário ou senha incorretos')
            return render(request, 'registration/login.html')

    else:
        # Se o método for diferente de POST, a página de login é renderizada
        return render(request, 'registration/login.html')