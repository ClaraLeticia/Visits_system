from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms import * 
from django.contrib import messages
from core.models import CustomUser

    
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
            login(request, user) # Loga o usuário
            if user.administrador: # Verifica se o usuário é administrador
                return redirect('/administrador') # Redireciona para a página de administrador
            if user.atendente: # Verifica se o usuário é atendente
                return redirect('/atendente') # Redireciona para a página de atendente
            if user.funcionario: # Verifica se o usuário é funcionário
                return redirect('/funcionario') # Redireciona para a página de funcionário
        
        else:
        # Se o usuário não for válido, uma mensagem de erro é exibida
            messages.info(request, 'Usuário ou senha incorretos')
            return render(request, 'registration/login.html')

    else:
        # Se o método for diferente de POST, a página de login é renderizada
        return render(request, 'registration/login.html')
    
# Função para deslogar o usuário e redirecionar para a página de login
def logoutView(request):
    logout(request)
    return redirect('/login')