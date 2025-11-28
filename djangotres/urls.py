from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

# 1. IMPORTAÇÕES NECESSÁRIAS PARA IMAGENS
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    
    # Seu app
    path('aura/', include('rede_aura.urls')),
]

# 2. CONFIGURAÇÃO PARA SERVIR ARQUIVOS DE MÍDIA (FOTOS)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)