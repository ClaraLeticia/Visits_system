# Projeto de Registro de Visitas

Este é um sistema de registro de visitas desenvolvido em Django. O sistema permite o cadastro de visitantes, funcionários e atendentes, além do gerenciamento de visitas.

## 🚀 Configuração do Projeto

### 1️⃣ **Pré-requisitos**
Antes de começar, certifique-se de ter instalado:
- Python 3.8+
- PostgreSQL
- Virtualenv (opcional, mas recomendado)

### 2️⃣ **Clonar o repositório**
```bash
 git clone https://github.com/ClaraLeticia/Visits_system.git
 cd Visits_system
 code . # Caso esteja utilizando o VS Code
```

### 3️⃣ **Criar e ativar o ambiente virtual**
```bash
python -m venv venv  # Criar ambiente virtual
source venv/bin/activate  # Ativar no Linux/macOS
venv\Scripts\activate  # Ativar no Windows
```

### 4️⃣ **Instalar dependências**
```bash
pip install -r requirements.txt
```

### 5️⃣ **Configurar o banco de dados**
```bash
python .\manage.py create_db 
```


### 6️⃣ **Criar as migrações e aplicar ao banco**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ **Popular o banco de dados com dados de teste**
O projeto inclui um comando customizado para popular o banco de dados.
```bash
python manage.py populate_db
```
Isso criará usuários administradores, atendentes e funcionários, além de visitantes e visitas fictícias.

### 8️⃣ **Iniciar o servidor**
```bash
python manage.py runserver
```
Acesse o sistema em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---
## 🔨 Instruções

1. Para login como **Administrador**, utilize o username `admin` e a senha `admin123`.
2. Para login como **Atendente**, utilize o username `atendente1` ou `atendente2` e as respectivas senhas (`atendente123` ou `atendente456`).
3. Para login como **Funcionário**, utilize o username `funcionario1` ou `funcionario2` e as respectivas senhas (`funcionario123` ou `funcionario456`).
---

## 📂 Estrutura do Projeto
```
Visist_system/
├── adminApp/        # Aplicação responsável pela lógica do administrador
│   ├── views.py
│   ├── urls.py
├── attendantApp/    # Aplicação responsável pela lógica do atendente
│   ├── views.py
│   ├── urls.py
├── employeeApp/     # Aplicação responsável pela lógica do funcionário
│   ├── views.py
│   ├── urls.py
├── core/            # Aplicação principal contendo os models e forms
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
├── system/          # Configurações gerais do Django
├── manage.py        # Comando para gerenciar o Django
├── requirements.txt # Dependências do projeto
├── media/           # Diretório para armazenar arquivos de mídia
├── static/          # Arquivos estáticos do projeto
├── templates/       # Templates HTML do projeto
└── README.md        # Documentação do projeto
```

---

## 🔧 Tecnologias Utilizadas
- **Django** (Framework principal)
- **PostgreSQL** (Banco de dados)
- **ImageKit** (Para processamento de imagens)
- **Django Guardian** (Controle de permissões)
- **Django Contrib Auth** (Autenticação)

---

📊 Inovações do Projeto

Uma das principais inovações deste sistema é a implementação de dashboards interativos com gráficos e cards para analisar o andamento das visitas. Essa funcionalidade permite visualizar métricas relevantes, como número de visitas realizadas, visitas que estão agendadas, número de visitas por setor e unidade, facilitando a gestão e tomada de decisões.

## 🛠 Possíveis Melhorias
- Implementar categoria de inatividade 
- Implementar filtros de busca


