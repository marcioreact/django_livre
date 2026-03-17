from django.urls import path
from . import views


urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path("alunos/", views.lista_alunos, name="lista_alunos"),

    path("alunos/novo/", views.criar_aluno, name="cadastro_aluno"),

    path("entrada/<int:id>/", views.registrar_entrada, name="entrada"),

    path("saida/<int:id>/", views.registrar_saida, name="saida"),

    path("acessos/", views.historico_acessos, name="historico"),

    path("imc/<int:id>/", views.calcular_imc, name="imc"),

    path("imc/", views.imc_dashboard, name="imc_dashboard"),

    path("pagamentos/", views.pagamentos, name="pagamentos"),

    path("pagar/<int:id>/", views.pagar_mensalidade, name="pagar"),
]