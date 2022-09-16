from django import forms
from django.db.models.fields import CharField

from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, ChoiceField

from aplicacionDB.models import Administrador, Solicitudes, Estudiante

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = '__all__'
        exclude = ('idAdmin',)
        MIS_CHOICES = (('SuperAdministrador', 'SuperAdministrador'), ('Administrador', 'Administrador'),('Recursos Financieros', 'Recursos Financieros'),)
        MIS_CHOICES2 = (('GENERAL', 'GENERAL'), ('ISC', 'ISC'), ('ITICS', 'ITICS'), ('ELECTRICA', 'ELECTRICA'), ('INSDUSTRIAL', 'INDUSTRIAL'),)
        widgets = {
            'nombres': TextInput(attrs={'class': 'form__field'}),
            'nombreUsuario': TextInput(attrs={'class':'form__field','name':'username'}),
            'apellidoPaterno': TextInput(attrs={'class':'form__field'}),
            'apellidoMaterno': TextInput(attrs={'class':'form__field'}),
            'telefono': NumberInput(attrs={'class':'form__field'}),
            'correo': EmailInput(attrs={'class':'form__field'}),
            'contraseña': PasswordInput(attrs={'class':'form__field','name':'password'}),
            'departamento': forms.Select(choices=MIS_CHOICES2,attrs={'class':'form__field'}),
            'rangoAdministrador': forms.Select(choices=MIS_CHOICES,attrs={'class':'form__field'})
        }

class SolicitudesForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = '__all__'
        MIS_CHOICES = (('1', 'Pendiente'), ('2', 'En proceso'), ('3', 'Concluido'),)
        widgets={
            'estatusAdministrador':forms.Select(choices=MIS_CHOICES, attrs={'class':'form-select'})
        }


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

