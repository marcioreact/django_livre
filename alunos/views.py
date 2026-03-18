from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Aluno, Acesso, Pagamento
from django.contrib import messages

def dashboard(request):

    total_alunos = Aluno.objects.count()

    presentes = Acesso.objects.filter(saida__isnull=True).count()

    return render(request, "alunos/dashboard.html", {
        "total_alunos": total_alunos,
        "presentes": presentes
    })

def lista_alunos(request):

    alunos = Aluno.objects.all()

    return render(request, "alunos/lista_alunos.html", {"alunos": alunos})

def criar_aluno(request):

    if request.method == "POST":

        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")

        Aluno.objects.create(
            nome=nome,
            email=email,
            telefone=telefone
        )

        return redirect("lista_alunos")

    return render(request, "alunos/form_aluno.html")

def registrar_entrada(request, id):

    aluno = get_object_or_404(Aluno, id=id)

    acesso_aberto = Acesso.objects.filter(
        aluno=aluno,
        saida__isnull=True
    ).exists()

    if not acesso_aberto:

        Acesso.objects.create(
            aluno=aluno,
            entrada=timezone.now()
        )

    return redirect("historico")

def registrar_saida(request, id):

    aluno = get_object_or_404(Aluno, id=id)

    acesso = Acesso.objects.filter(
        aluno=aluno,
        saida__isnull=True
    ).last()

    if acesso:

        acesso.saida = timezone.now()
        acesso.save()

    return redirect("historico")

def historico_acessos(request):

    acessos = Acesso.objects.select_related("aluno").order_by("-entrada")

    return render(request, "alunos/historico.html", {
        "acessos": acessos
    })

def calcular_imc(request, id):

    aluno = get_object_or_404(Aluno, id=id)

    if request.method == "POST":

        peso = float(request.POST.get("peso"))
        altura = float(request.POST.get("altura"))

        imc = peso / (altura ** 2)

        if imc < 18.5:
            classificacao = "Abaixo do peso"
            exercicio = "Musculação leve"

        elif imc < 25:
            classificacao = "Peso normal"
            exercicio = "Treino completo"

        elif imc < 30:
            classificacao = "Sobrepeso"
            exercicio = "Cardio e musculação"

        else:
            classificacao = "Obesidade"
            exercicio = "Caminhada e bicicleta"

        return render(request, "alunos/imc.html", {
            "aluno": aluno,
            "imc": round(imc, 2),
            "classificacao": classificacao,
            "exercicio": exercicio
        })

    return render(request, "alunos/imc.html", {"aluno": aluno})

def imc_dashboard(request):
    aluno = None
    
    if request.method == "POST":

        peso = float(request.POST.get("peso"))
        altura = float(request.POST.get("altura"))

        imc = peso / (altura ** 2)

        if imc < 18.5:
            classificacao = "Abaixo do peso"
            exercicio = "Musculação leve"

        elif imc < 25:
            classificacao = "Peso normal"
            exercicio = "Treino completo"

        elif imc < 30:
            classificacao = "Sobrepeso"
            exercicio = "Cardio e musculação"

        else:
            classificacao = "Obesidade"
            exercicio = "Caminhada e bicicleta"

        return render(request, "alunos/imc.html", {
            "aluno": aluno,
            "imc": round(imc, 2),
            "classificacao": classificacao,
            "exercicio": exercicio
        })

    return render(request, "alunos/imc.html")

def pagamentos(request):

    alunos = Aluno.objects.all()

    status_alunos = []

    for aluno in alunos:

        ultimo_pagamento = Pagamento.objects.filter(
            aluno=aluno
        ).order_by("-data_pagamento").first()

        if ultimo_pagamento and ultimo_pagamento.ativo():

            status = "ativo"

        else:

            status = "desativado"

        status_alunos.append({
            "aluno": aluno,
            "status": status
        })

    return render(request, "alunos/pagamentos.html", {
        "status_alunos": status_alunos
    })

def pagar_mensalidade(request, id):
    aluno = get_object_or_404(Aluno, id=id)

    
    Pagamento.objects.create(
        aluno=aluno,
        valor=100.00,
        data_pagamento=timezone.now()
    )

    messages.success(request, f"Pagamento de {aluno.nome} registrado!")
    return redirect("pagamentos")


def deletar_aluno(request, id):

    aluno = get_object_or_404(Aluno, id=id)

    if request.method == "POST":
        aluno.delete()
        return redirect("lista_alunos")

    return render(request, "alunos/confirmar_delete.html", {
        "aluno": aluno
    })

