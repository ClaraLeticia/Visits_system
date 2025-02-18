from django.core.exceptions import ValidationError

# Classe para validar a senha do usuário
class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if password.isdigit():
            raise ValidationError("A senha não pode conter apenas números.")
        if password.lower() in ['12345678', 'senha123', 'qwerty', 'abcdefg']:
            raise ValidationError("Essa senha é muito comum. Escolha outra senha.")

    def get_help_text(self):
        return ("A senha deve ter pelo menos 8 caracteres e não pode ser totalmente numérica ou comum.")

# Função para validar o RG
def validate_rg(value):
    if len(value) != 9:
        raise ValidationError('O RG deve ter 9 dígitos')
    
# Função para validar o CPF
def validate_cpf(value):
    if len(value) != 11:
        raise ValidationError('O CPF deve ter 11 dígitos')

# Função para validar o telefone
def validate_phone(value):
    if len(value) != 11:
        raise ValidationError('O Telefone deve ter 11 dígitos')


# Não foram colocadas as funções de validação de e-mail e nome de usuário, pois o Django já possui validações para esses campos.
# Não foram colocadas validações mais aprofundadas para cpf e rg para não complicar o exemplo.