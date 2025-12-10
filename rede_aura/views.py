from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from .models import Profissional, CasaAcolhimento, DireitoInfo, AreaAtendimento, Agendamento
from .models import Profissional

# --- IMPORTS DE FORMULÁRIOS ---
# Tenta importar o formulário de cadastro personalizado
try:
    from usuarios.forms import ModelUsuarioCreateForm as CadastroForm
except ImportError:
    from django.contrib.auth.forms import UserCreationForm as CadastroForm

# Importa o formulário de edição de perfil
from .forms import EditarPerfilForm

# --- IMPORTS DE MODELOS ---
from .models import (
    Postagem, Comentario, ConteudoEducativo, LocalApoio, Profissional,
    Agendamento, PlanoSeguranca, ContatoEmergencia,
    MedidaProtetiva, Alerta
)

# ==========================================
# 1. AUTENTICAÇÃO E ONBOARDING
# ==========================================

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loga o usuário

            # Cria o Plano de Segurança (Termo não aceito ainda)
            PlanoSeguranca.objects.create(usuario=user, termo_aceito=False)

            return redirect('termo_aceite')  # Manda para o Termo
    else:
        form = CadastroForm()
    return render(request, 'registration/cadastro.html', {'form': form})


@login_required
def termo_aceite(request):
    plano, created = PlanoSeguranca.objects.get_or_create(usuario=request.user)

    if plano.termo_aceito:
        return redirect('feed')

    if request.method == 'POST':
        plano.termo_aceito = True
        plano.data_aceite_termo = timezone.now()
        plano.save()
        return redirect('feed')

    return render(request, 'registration/termo.html')


# ==========================================
# 2. DASHBOARD (INÍCIO)
# ==========================================

@login_required
def feed(request):
    # Verificação de Segurança do Termo
    plano, created = PlanoSeguranca.objects.get_or_create(usuario=request.user)
    if not plano.termo_aceito:
        return redirect('termo_aceite')

    # Dados para os cards do Dashboard
    medidas_ativas = MedidaProtetiva.objects.filter(usuario=request.user, ativa=True).count()
    alertas_hoje = Alerta.objects.filter(usuario=request.user, lido=False).count()

    context = {
        'plano': plano,
        'medidas': medidas_ativas,
        'alertas': alertas_hoje,
    }
    return render(request, 'rede_aura/feed.html', context)


# ==========================================
# 3. COMUNIDADE E INTERAÇÕES
# ==========================================

@login_required
def comunidade(request):
    # Garante que o plano existe para o user atual
    plano, created = PlanoSeguranca.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        Postagem.objects.create(
            autor=request.user,
            texto=request.POST.get('texto'),
            categoria=request.POST.get('categoria')
        )
        return redirect('comunidade')

    posts = Postagem.objects.all().order_by('-data_criacao')
    return render(request, 'rede_aura/comunidade.html', {
        'posts': posts,
        'plano': plano,              # passa o plano também
    })



@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Postagem, id=post_id)
    post.curtidas += 1
    post.save()
    return redirect('comunidade')


@login_required
def excluir_post(request, post_id):
    post = get_object_or_404(Postagem, id=post_id)
    if request.user == post.autor:
        post.delete()
    return redirect('comunidade')


@login_required
def comentar_post(request, post_id):
    post = get_object_or_404(Postagem, id=post_id)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        if texto:
            Comentario.objects.create(postagem=post, autor=request.user, texto=texto)
    return redirect('comunidade')


# ==========================================
# 4. FUNCIONALIDADES DO SISTEMA
# ==========================================

@login_required
def educacao(request):
    conteudos = ConteudoEducativo.objects.filter(tipo__in=['VIDEO', 'ARTIGO'])
    workshops = ConteudoEducativo.objects.filter(tipo='WORKSHOP')
    return render(request, 'rede_aura/educacao.html', {'conteudos': conteudos, 'workshops': workshops})


@login_required
def mapa(request):
    locais = LocalApoio.objects.all()
    return render(request, 'rede_aura/mapa.html', {'locais': locais})


@login_required
def apoio(request):
    area = request.GET.get('area')
    if area:
        profissionais = Profissional.objects.filter(area=area)
    else:
        profissionais = Profissional.objects.all()
    return render(request, 'rede_aura/apoio.html', {'profissionais': profissionais})


@login_required
def agendar(request, profissional_id):
    profissional = get_object_or_404(Profissional, id=profissional_id)
    if request.method == 'POST':
        Agendamento.objects.create(
            usuario=request.user,
            profissional=profissional,
            data=request.POST.get('data'),
            hora=request.POST.get('hora')
        )
        return render(request, 'rede_aura/agendamento_sucesso.html', {'profissional': profissional})
    return render(request, 'rede_aura/agendar.html', {'profissional': profissional})


@login_required
def emergencia(request):
    # Garante que o plano existe
    plano, created = PlanoSeguranca.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        # Verifica se é o formulário de novo contato (campo hidden)
        if 'novo_contato' in request.POST:
            nome = request.POST.get('nome')
            telefone = request.POST.get('telefone')
            parentesco = request.POST.get('parentesco')

            if nome and telefone:
                ContatoEmergencia.objects.create(
                    plano=plano,
                    nome=nome,
                    telefone=telefone,
                    parentesco=parentesco
                )
                # IMPORTANTE: Redireciona para a mesma página para limpar o form e atualizar a lista
                return redirect('emergencia')

        elif 'config_plano' in request.POST:
            plano.mensagem_emergencia = request.POST.get('mensagem')
            plano.localizacao_automatica = 'localizacao' in request.POST
            plano.save()
            return redirect('emergencia')

    return render(request, 'rede_aura/emergencia.html', {'plano': plano})


@login_required
def medidas(request):
    medidas = MedidaProtetiva.objects.filter(usuario=request.user).order_by('-ativa', 'data_validade')
    return render(request, 'rede_aura/medidas.html', {'medidas': medidas})


@login_required
def alertas(request):
    notificacoes = Alerta.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'rede_aura/alertas.html', {'notificacoes': notificacoes})


@login_required
def termos(request):
    return render(request, 'rede_aura/termos.html')  # Caso tenha criado a aba separada


# ==========================================
# 5. PERFIL E EDIÇÃO
# ==========================================

@login_required
def perfil(request):
    return render(request, 'rede_aura/perfil.html', {'user': request.user})


@login_required
def editar_perfil(request):
    plano, created = PlanoSeguranca.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=plano)
        if form.is_valid():
            plano = form.save()

            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.fone = form.cleaned_data['fone']

            # se ModelUsuario tiver campo foto, sincroniza
            if hasattr(user, "foto") and plano.foto:
                user.foto = plano.foto

            user.save()
            return redirect('perfil')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'fone': getattr(request.user, 'fone', ''),
        }
        form = EditarPerfilForm(instance=plano, initial=initial_data)

    return render(request, 'rede_aura/editar_perfil.html', {
        'form': form,
        'plano': plano,
    })



@login_required
def editar_contato(request, contato_id):
    # Busca o contato apenas se ele pertencer ao plano do usuário logado (Segurança)
    contato = get_object_or_404(ContatoEmergencia, id=contato_id, plano__usuario=request.user)

    if request.method == 'POST':
        # Atualiza os dados
        contato.nome = request.POST.get('nome')
        contato.telefone = request.POST.get('telefone')
        contato.parentesco = request.POST.get('parentesco')
        contato.save()
        return redirect('emergencia')  # Volta para a lista

    # Se for GET, renderiza a página de edição
    return render(request, 'rede_aura/editar_contato.html', {'contato': contato})


@login_required
def excluir_contato(request, contato_id):
    # Busca o contato garantindo que pertence ao usuário
    contato = get_object_or_404(ContatoEmergencia, id=contato_id, plano__usuario=request.user)
    contato.delete()
    return redirect('emergencia')


@login_required
def apoio(request):
    areas = AreaAtendimento.objects.all()
    casas = CasaAcolhimento.objects.all()

    # Contatos recomendados fixos (como no vídeo)
    contatos_uteis = [
        {'nome': 'Polícia Militar', 'numero': '190', 'desc': 'Emergência 24h'},
        {'nome': 'Central da Mulher', 'numero': '180', 'desc': 'Denúncias e apoio'},
        {'nome': 'SAMU', 'numero': '192', 'desc': 'Emergências médicas'},
    ]

    context = {
        'areas': areas,
        'casas': casas,
        'contatos_uteis': contatos_uteis
    }
    return render(request, 'rede_aura/apoio.html', context)


@login_required
def agendar_consulta(request):
    if request.method == 'POST':
        profissional_id = request.POST.get('profissional')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        tipo = request.POST.get('tipo_atendimento')

        from datetime import datetime
        # Combina data e hora (formato YYYY-MM-DD HH:MM)
        data_hora_str = f"{data} {hora}"
        data_hora_obj = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')

        profissional = get_object_or_404(Profissional, id=profissional_id)

        novo_agendamento = Agendamento.objects.create(
            usuario=request.user,
            profissional=profissional,
            data_hora=data_hora_obj,
            tipo=tipo,
            status='CONFIRMADO'  # Define o status inicial
        )
        # Redireciona para a tela de sucesso com o ID do novo agendamento
        return redirect('agendamento_sucesso', agendamento_id=novo_agendamento.id)

    # GET: Mostra o formulário
    profissionais = Profissional.objects.filter(disponivel=True)
    return render(request, 'rede_aura/agendar.html', {'profissionais': profissionais})


# NOVA FUNÇÃO: PARA EXIBIR A TELA DE SUCESSO
@login_required
def agendamento_sucesso(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    return render(request, 'rede_aura/agendamento_sucesso.html', {'agendamento': agendamento})


@login_required
def lista_direitos(request):
    direitos = DireitoInfo.objects.all()
    return render(request, 'rede_aura/seus_direitos.html', {'direitos': direitos})


@login_required
def meus_agendamentos(request):
    # Busca agendamentos ativos, ordenados do mais antigo para o mais novo
    agendamentos = Agendamento.objects.filter(
        usuario=request.user
    ).exclude(
        status__in=['CANCELADO', 'FINALIZADO']
    ).order_by('data_hora')

    return render(request, 'rede_aura/meus_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def lista_profissionais(request):
    profissionais = Profissional.objects.filter(disponivel=True)
    return render(request, 'rede_aura/profissionais.html', {'profissionais': profissionais})