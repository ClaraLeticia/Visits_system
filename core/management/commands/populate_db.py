from django.core.management.base import BaseCommand
from core.models import Branch, Department, CustomUser, Visitor, Visits
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Criando unidades
        branch1 = Branch.objects.create(name="Filial Centro", description="Unidade central")
        branch2 = Branch.objects.create(name="Filial Norte", description="Unidade da zona norte")
    
        # Criando departamentos
        dept1 = Department.objects.create(name="RH", branch=branch1, description="Departamento de Recursos Humanos")
        dept2 = Department.objects.create(name="TI", branch=branch1, description="Departamento de Tecnologia da Informação")
        dept3 = Department.objects.create(name="Segurança", branch=branch2, description="Departamento de Segurança")
    
        # Criando usuários
        admin_user = CustomUser.objects.create_user(email="admin@email.com", username="admin", password="admin123", administrador=True, phone="11987654321")
        attendant_user1 = CustomUser.objects.create_user(email="atendente1@email.com", username="atendente1", password="atendente123", atendente=True, phone="11987654322", branch=branch1)
        attendant_user2 = CustomUser.objects.create_user(email="atendente2@email.com", username="atendente2", password="atendente456", atendente=True, phone="11987654326", branch=branch2)
        employee_user1 = CustomUser.objects.create_user(email="funcionario1@email.com", username="funcionario1", password="funcionario123", funcionario=True, phone="11987654323", branch=branch1, department=dept1)
        employee_user2 = CustomUser.objects.create_user(email="funcionario2@email.com", username="funcionario2", password="funcionario456", funcionario=True, phone="11987654327", branch=branch2, department=dept3)
    
        # Criando visitantes
        visitor1 = Visitor.objects.create(cpf="12345678901", rg="12345678", name="João Silva", phone="11987654324")
        visitor2 = Visitor.objects.create(cpf="98765432100", rg="87654321", name="Maria Souza", phone="11987654325")
        visitor3 = Visitor.objects.create(cpf="56789012345", rg="56789012", name="Carlos Oliveira", phone="11987654328")
        visitor4 = Visitor.objects.create(cpf="23456789012", rg="23456789", name="Ana Pereira", phone="11987654329")
    
        # Criando visitas (funcionários só podem registrar visitas na sua branch)
        visit1 = Visits.objects.create(status="Aguardando", visitor=visitor1, user=employee_user1, department=dept1, date=now())
        visit2 = Visits.objects.create(status="Aguardando", visitor=visitor2, user=employee_user1, department=dept2, date=now())
        visit3 = Visits.objects.create(status="Aguardando", visitor=visitor3, user=employee_user2, department=dept3, date=now())
        visit4 = Visits.objects.create(status="Aguardando", visitor=visitor4, user=employee_user2, department=dept3, date=now())
    
        self.stdout.write(self.style.SUCCESS("Dados de teste criados com sucesso!"))