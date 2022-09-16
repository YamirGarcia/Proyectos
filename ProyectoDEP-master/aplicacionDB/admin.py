from django.contrib import admin

# Register your models here.
from aplicacionDB.models import Estudiante, Administrador, Referencia, Solicitudes, Documentos, Tramites

admin.site.register(Estudiante)
admin.site.register(Administrador)
admin.site.register(Solicitudes)
admin.site.register(Documentos)
admin.site.register(Tramites)
admin.site.register(Referencia)