from typing import Text
from django import forms
# from django.db.models.fields import CharField

from django.forms import TextInput
from django.forms import widgets
from django.forms.widgets import EmailInput, FileInput, NumberInput, PasswordInput

from aplicacionDB.models import Documentos, Estudiante

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'
        MIS_CHOICES = (('ISC', 'ISC'), ('ITICS', 'ITICS'), ('ELECTRICA', 'ELECTRICA'), ('INSDUSTRIAL', 'INDUSTRIAL'),)
        widgets = {
            'numeroControl':TextInput(attrs={'class':'form__field'}),
            'nombres':TextInput(attrs={'class':'form__field'}),
            'apellidoPaterno':TextInput(attrs={'class':'form__field'}),
            'apellidoMaterno':TextInput(attrs={'class':'form__field'}),
            'carrera':forms.Select(choices=MIS_CHOICES, attrs={'class':'form__field'}),
            'correo': EmailInput(attrs={'class':'form__field'}),
            'contraseña': PasswordInput(attrs={'class':'form__field'})
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = '__all__'
        # exclude = ('',)
        # MIS_CHOICES = (('1', 'SuperAdministrador'), ('2', 'Administrador'),)
        widgets = {
            'numeroFolio': TextInput(attrs={'class': 'form-control'}),
            'numeroControl': TextInput(attrs={'class': 'form-control'}),
            'archivos': FileInput(attrs={})

        }

# class User