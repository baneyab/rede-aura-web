from django import forms
from .models import PlanoSeguranca
from usuarios.models import ModelUsuario # Importe o usuário original

class EditarPerfilForm(forms.ModelForm):
    # Campos do Usuário (Nome, Email, Telefone)
    first_name = forms.CharField(label="Nome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    fone = forms.CharField(label="Telefone", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PlanoSeguranca
        fields = ['cpf', 'data_nascimento', 'endereco', 'foto']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
        }