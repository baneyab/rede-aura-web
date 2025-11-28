from django.db import models
from django.conf import settings

# ==========================================
# 1. MODELOS DE APOIO (Áreas, Casas, Direitos)
# ==========================================

class AreaAtendimento(models.Model):
    nome = models.CharField(max_length=100)  # Ex: Psicológico, Jurídico
    icone = models.CharField(max_length=50)  # Ex: fas fa-brain

    def __str__(self):
        return self.nome


class CasaAcolhimento(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    vagas_disponiveis = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class DireitoInfo(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(
        max_length=50,
        choices=[
            ('TRABALHISTA', 'Trabalhista'),
            ('CIVIL', 'Civil'),
            ('PENAL', 'Penal'),
        ]
    )

    def __str__(self):
        return self.titulo


# ==========================================
# 2. PROFISSIONAIS E AGENDAMENTO
# ==========================================

class Profissional(models.Model):
    nome = models.CharField(max_length=100)
    profissao = models.CharField(max_length=100)  # Ex: Psicóloga
    registro = models.CharField(max_length=50)    # Ex: CRP 12/3456
    # Vínculo com a tabela de Áreas
    area = models.ForeignKey(AreaAtendimento, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='profissionais/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    # Usando settings.AUTH_USER_MODEL para evitar erros
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    tipo = models.CharField(
        max_length=20,
        choices=[('ONLINE', 'Online'), ('PRESENCIAL', 'Presencial')]
    )
    status = models.CharField(max_length=20, default='PENDENTE')

    def __str__(self):
        return f"Agendamento de {self.usuario} com {self.profissional}"


# ==========================================
# 3. FEED E COMUNIDADE
# ==========================================

class Postagem(models.Model):
    CATEGORIAS = [
        ('RELATO', 'Relato'),
        ('MOTIVACAO', 'Motivação'),
        ('AJUDA', 'Pedido de Ajuda'),
    ]
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    data_criacao = models.DateTimeField(auto_now_add=True)
    curtidas = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.autor} - {self.categoria}"


class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.postagem}"


# ==========================================
# 4. CONTEÚDOS E LOCAIS
# ==========================================

class ConteudoEducativo(models.Model):
    TIPOS = [
        ('VIDEO', 'Vídeo'),
        ('ARTIGO', 'Artigo'),
        ('PODCAST', 'Podcast'),
    ]
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    duracao = models.CharField(max_length=20, help_text="Ex: 5 min")
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, default="Direitos")
    link_conteudo = models.URLField()

    def __str__(self):
        return self.titulo


class LocalApoio(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)
    telefone = models.CharField(max_length=20)
    horario = models.CharField(max_length=100, default="08h às 18h")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome


# ==========================================
# 5. SEGURANÇA E ALERTAS
# ==========================================

class MedidaProtetiva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    numero_processo = models.CharField(max_length=50)
    data_validade = models.DateField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Alerta(models.Model):
    TIPOS = [
        ('AVISO', 'Aviso'),
        ('SISTEMA', 'Sistema'),
        ('CHECKIN', 'Check-in'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='SISTEMA')
    data = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class PlanoSeguranca(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Campos de Segurança
    mensagem_emergencia = models.TextField(
        default="Estou em perigo, por favor, ajude! Minha localização atual é..."
    )
    localizacao_automatica = models.BooleanField(default=False)
    modo_disfarcado = models.BooleanField(default=False)

    # Campos do Termo
    termo_aceito = models.BooleanField(default=False)
    data_aceite_termo = models.DateTimeField(null=True, blank=True)

    # Campos de Perfil
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario}"


class ContatoEmergencia(models.Model):
    plano = models.ForeignKey(PlanoSeguranca, related_name='contatos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    parentesco = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
