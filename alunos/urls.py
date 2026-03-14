from django.urls import path
from . import views

urlpatterns = [

    path('imc/', views.calcular_imc, name="imc"),
    path('', views.dashboard, name="dashboard"),

    path('alunos/', views.lista_alunos, name="lista_alunos"),

    path('alunos/novo/', views.criar_aluno, name="criar_aluno"),

    path('alunos/delete/<int:id>/', views.deletar_aluno, name="deletar_aluno"),

   
]