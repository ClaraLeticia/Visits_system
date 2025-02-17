from django.core.exceptions import ValidationError

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

def validate_rg(value):
    if len(value) != 9:
        raise ValidationError('O RG deve ter 9 dígitos')
    
def validate_cpf(value):
    if len(value) != 9:
        raise ValidationError('O CPF deve ter 11 dígitos')

def validate_phone(value):
    if len(value) != 9:
        raise ValidationError('O Telefone deve ter 11 dígitos')

def validate_password(value):
    if len(value) != 9:
        raise ValidationError('Senha deve ter 8 caracteres.\n.Senha muito comum.\nSenha deve conter letras')
