# Rede Aura Web

Prototipagem da plataforma Rede Aura para versão web, focada em apoio a mulheres em situação de violência, oferecendo uma experiência segura para acesso a informações, rede de apoio e serviços especializados.

## ✨ Funcionalidades principais

- Dashboard com visão geral do usuário autenticado.
- Rede de Apoio:
  - Agendar atendimento com profissionais cadastrados.
  - Listar profissionais por área de atendimento.
  - Visualizar casas de acolhimento e contatos recomendados.
- Comunidade:
  - Publicar relatos e pedidos de ajuda.
  - Curtir e comentar postagens.
- Educação:
  - Listagem de conteúdos educativos (vídeos, artigos, etc.).
- Seus Direitos:
  - Página informativa com principais direitos e garantias.
- Medidas Protetivas:
  - Cadastro e visualização de medidas protetivas do usuário.
- Alertas:
  - Lista de alertas/notificações relacionados à segurança.
- Plano de Segurança:
  - Configuração de mensagem de emergência, contatos e preferências.
- Perfil:
  - Edição de dados pessoais e foto de perfil.

## 🛠️ Tecnologias utilizadas

- Python (Django)
- HTML, CSS, Bootstrap
- JavaScript (uso leve para interações)
- SQLite (banco padrão de desenvolvimento do Django)

## 🚀 Como executar o projeto

1. Clonar o repositório:

git clone https://github.com/baneyab/rede-aura-web.git
cd rede-aura-web

text

2. Criar e ativar o ambiente virtual:

python -m venv venv
venv\Scripts\activate # Windows

ou
source venv/bin/activate # Linux/Mac

text

3. Instalar as dependências:

pip install -r requirements.txt

text

4. Rodar as migrações:

python manage.py migrate

text

5. Criar um usuário administrador (opcional):

python manage.py createsuperuser

text

6. Iniciar o servidor de desenvolvimento:

python manage.py runserver

text

Depois, acesse em `http://127.0.0.1:8000/`.

## 📂 Estrutura principal

- `rede_aura/` – app principal (views, models, templates).
- `templates/rede_aura/` – páginas HTML do dashboard e fluxos da aplicação.
- `static/` – arquivos estáticos (CSS, JS, imagens) quando configurados.
- `manage.py` – script principal do projeto Django.

## ✅ Status do projeto

Projeto em fase de prototipagem e testes.  
Rotas principais, telas e fluxo de agendamento/apoio já estão sendo construídos e refinados.

## 📄 Licença

Projeto acadêmico/didático.
