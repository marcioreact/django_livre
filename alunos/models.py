from django.db import models
from django.utils import timezone
from datetime import timedelta


class Aluno(models.Model):

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Acesso(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

    entrada = models.DateTimeField()

    saida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.entrada}"


class Pagamento(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

    data_pagamento = models.DateField(default=timezone.now)

    valor = models.DecimalField(max_digits=8, decimal_places=2)

    ativo = models.BooleanField(default=True)

    def ativo(self):

        validade = self.data_pagamento + timedelta(days=30)

        return timezone.now().date() <= validade