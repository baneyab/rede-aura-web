from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('cadastro/', views.cadastro, name='cadastro'),

    # Telas do Sistema
    path('feed/', views.feed, name='feed'),
    path('comunidade/', views.comunidade, name='comunidade'),
    path('educacao/', views.educacao, name='educacao'),
    path('mapa/', views.mapa, name='mapa'),
    path('apoio/', views.apoio, name='apoio'),
    path('agendar/<int:profissional_id>/', views.agendar, name='agendar'),
    path('emergencia/', views.emergencia, name='emergencia'),
    path('perfil/', views.perfil, name='perfil'),
    path('medidas/', views.medidas, name='medidas'),
    path('alertas/', views.alertas, name='alertas'),
    path('termo/', views.termo_aceite, name='termo_aceite'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('post/<int:post_id>/curtir/', views.curtir_post, name='curtir_post'),
    path('post/<int:post_id>/excluir/', views.excluir_post, name='excluir_post'),
    path('post/<int:post_id>/comentar/', views.comentar_post, name='comentar_post'),
    path('emergencia/editar/<int:contato_id>/', views.editar_contato, name='editar_contato'),
    path('emergencia/excluir/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),

    # Rede de Apoio
    path('apoio/', views.apoio, name='apoio'),
    path('apoio/agendar/', views.agendar_consulta, name='agendar_consulta'),
    path('apoio/agendar/sucesso/<int:agendamento_id>/', views.agendamento_sucesso, name='agendamento_sucesso'),
    path('apoio/direitos/', views.lista_direitos, name='lista_direitos'),
    path('apoio/meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
    path('apoio/profissionais/', views.lista_profissionais, name='lista_profissionais'),
]
