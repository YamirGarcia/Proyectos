from datetime import date
import os
from django.db import models


# Create your models here.
class Estudiante(models.Model):
    numeroControl = models.CharField(max_length=10)
    nombres = models.CharField(max_length=255)
    apellidoPaterno = models.CharField(max_length=255)
    apellidoMaterno = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    contraseña = models.CharField(max_length=20)

    def __str__(self):
        return f'Estudiantes: {self.numeroControl} {self.nombres} {self.apellidoPaterno} {self.apellidoMaterno} {self.carrera} {self.contraseña}'


class Administrador(models.Model):
    nombreUsuario = models.CharField(max_length=255)
    contraseña = models.CharField(max_length=20)
    correo = models.CharField(max_length=255)
    nombres = models.CharField(max_length=255)
    apellidoMaterno = models.CharField(max_length=255)
    apellidoPaterno = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)
    rangoAdministrador = models.CharField(max_length=255)

    def __str__(self):
        return f'Administradores: {self.idAdmin} {self.nombreUsuario} {self.contraseña} {self.rangoAdministrador}'

class Tramites(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

class Solicitudes(models.Model):
    numeroControl = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True)
    numeroFolio = models.CharField(max_length=255)
    estatusAlumno = models.CharField(max_length=255)
    estatusAdministrador = models.CharField(max_length=255)
    comentarios = models.CharField(max_length=255, null=True)
    fechaCreacion = models.DateField()
    fechaCierre = models.DateField(null=True)
    tipoTramite = models.ForeignKey(Tramites, on_delete=models.SET_NULL, null=True)
    dictamen = models.FileField(blank=True, upload_to='dictaminados', max_length=255)

    def __str__(self):
        return f'Solicitudes: {self.numeroControl} {self.numeroFolio} {self.estatusAlumno} {self.estatusAdministrador}'

    def nombre_dictaminado(self):
        return os.path.basename(self.dictamen.name)

class Archivos (models.Model):
    documento = models.FileField(blank=True, upload_to='documentos', max_length=255)
    numeroFolio = models.ForeignKey(Solicitudes, on_delete=models.SET_NULL, null=True)

    def filename(self):
        return os.path.basename(self.documento.name)

class Documentos(models.Model):
    numeroFolio = models.ForeignKey(Solicitudes, on_delete=models.SET_NULL, null=True)
    numeroControl = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True)
    archivos = models.FileField(blank=True, upload_to='documentos', max_length=255)

    def __str__(self):
        return f'Documentos: {self.id} {self.numeroFolio} {self.archivo}'

class Referencia(models.Model):
    numeroControl = models.CharField(max_length=255)
    nombres =  models.CharField(max_length=255)
    tipoTramite = models.CharField(max_length=255)
    correo =  models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)

    def __str__(self):
        return f'Referencias: {self.numeroControl} {self.nombres} {self.carrera} {self.tipoTramite} {self.correo} {self.carrera}'
