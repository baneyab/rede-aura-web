from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    PlanoSeguranca, ContatoEmergencia, MedidaProtetiva, Alerta, 
    Postagem, Comentario, ConteudoEducativo, LocalApoio,
    AreaAtendimento, Profissional, CasaAcolhimento, DireitoInfo, Agendamento
)

# Configurações para exibir melhor no Admin

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'profissao', 'area', 'disponivel')
    list_filter = ('area', 'disponivel')

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'profissional', 'data_hora', 'status')
    list_filter = ('status', 'data_hora')

@admin.register(CasaAcolhimento)
class CasaAcolhimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'vagas_disponiveis')

# Registrando os outros modelos simples
admin.site.register(PlanoSeguranca)
admin.site.register(ContatoEmergencia)
admin.site.register(MedidaProtetiva)
admin.site.register(Alerta)
admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(ConteudoEducativo)
admin.site.register(LocalApoio)
admin.site.register(AreaAtendimento)
admin.site.register(DireitoInfo)