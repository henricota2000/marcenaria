from django.db import models
from django.core.exceptions import ValidationError
import re
import datetime


# Validação para CPF
def validate_cpf(value):
    cpf_pattern = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    if not re.match(cpf_pattern, value):
        raise ValidationError('CPF deve estar no formato XXX.XXX.XXX-XX')

# Validação para telefone
def validate_telefone(value):
    telefone_pattern = r'^\(\d{2}\) \d{4,5}-\d{4}$'
    if not re.match(telefone_pattern, value):
        raise ValidationError('Telefone deve estar no formato (XX) XXXXX-XXXX')

# Validação para data de nascimento
def validate_date(value):
    if value and value > datetime.date.today():
        raise ValidationError('A data de nascimento não pode ser no futuro.')

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf], blank=True,default="000.000.000-00")  # Define um valor padrão
    rg = models.CharField(max_length=12, unique=True, default="000000000")  # Define um valor padrão
    data_nascimento = models.DateField(null=True) # formato dd/mm/aaaa
    cep = models.CharField(max_length=9, default="00000-000")  # Define um valor padrão
    endereco = models.CharField(max_length=255, default="Não informado")  # Define um valor padrão
    numero = models.CharField(max_length=10, default="S/N")  # Define um valor padrão
    complemento = models.CharField(max_length=100, default="Nenhum")  # Define um valor padrão
    cidade = models.CharField(max_length=100, default="Desconhecida")  # Define um valor padrão
    estado = models.CharField(max_length=2, default="XX")  # Define um valor padrão
    telefone1 = models.CharField(max_length=15, blank=True, default="Não informado")  # Define um valor padrão
    telefone2 = models.CharField(max_length=15, blank=True, default="Não informado")  # Define um valor padrão
    email = models.EmailField(blank=True) ## Permitir valores nulos temporariamente
    historico_pedidos = models.TextField(blank=True, default="")  # Define um valor padrão

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  #  Use 'Cliente' como string
    descricao = models.TextField(blank=True)
    data_pedido = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"
