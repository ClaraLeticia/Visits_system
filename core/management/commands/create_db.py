from django.core.management.base import BaseCommand
from core.models import Branch, Department, CustomUser, Visitor, Visits
from django.utils.timezone import now
import psycopg2
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Criando conexão com o banco de dados
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        conn.autocommit = True # Garante que o comando CREATE DATABASE seja executado
        cursor = conn.cursor() # Cursor para executar comandos SQL

        # Verifica se o banco de dados já existe
        db_name = settings.DATABASES["default"]["NAME"]
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
    
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            # Criação do banco de dados
            print(f"Banco de dados '{db_name}' criado com sucesso!")
        else:
            print(f"Banco de dados '{db_name}' já existe.")

        # Fechando conexão com o banco de dados
        cursor.close()
        conn.close()
        
        self.stdout.write(self.style.SUCCESS("Banco de dados criado com sucesso!"))