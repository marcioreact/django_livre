from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlunoForm
from django.contrib.auth.decorators import login_required
from .models import Aluno


@login_required
def dashboard(request):
    total_alunos = Aluno.objects.count()
    return render(request, "alunos/dashboard.html", {
        "total_alunos": total_alunos,        
    })


@login_required
def lista_alunos(request):


    alunos = Aluno.objects.all()

    return render(request, "alunos/lista_alunos.html", {"alunos": alunos})


@login_required
def criar_aluno(request):

    form = AlunoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("lista_alunos")

    return render(request, "alunos/form_aluno.html", {"form": form})


@login_required
def deletar_aluno(request, id):

    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()

    return redirect("lista_alunos")


@login_required
def calcular_imc(request):

    imc = None
    classificacao = None
    exercicio = None

    if request.method == "POST":

        try:

            peso = float(request.POST.get("peso"))
            altura = float(request.POST.get("altura"))

            imc = peso / (altura ** 2)
            imc = round(imc, 2)

            if imc < 18.5:
                classificacao = "Abaixo do peso"
                exercicio = "Treinos de força e musculação para ganho de massa."

            elif 18.5 <= imc < 25:
                classificacao = "Peso normal"
                exercicio = "Treino equilibrado com musculação e cardio moderado."

            elif 25 <= imc < 30:
                classificacao = "Sobrepeso"
                exercicio = "Cardio regular (corrida, bicicleta) e treino funcional."

            elif 30 <= imc < 35:
                classificacao = "Obesidade Grau I"
                exercicio = "Caminhada, bicicleta e musculação leve."

            elif 35 <= imc < 40:
                classificacao = "Obesidade Grau II"
                exercicio = "Exercícios de baixo impacto com acompanhamento."

            else:
                classificacao = "Obesidade Grau III"
                exercicio = "Atividade física supervisionada e exercícios leves."

        except:
            classificacao = "Erro nos dados informados"

    return render(request, "alunos/imc.html", {
        "imc": imc,
        "classificacao": classificacao,
        "exercicio": exercicio
    })