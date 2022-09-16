"""ProyectoDEP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django import urls
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, logout_then_login
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls.conf import re_path
from django.views.static import serve

from aplicacionAdministrador.views import administrar_usuarios, detalle_solicitud, detalle_solicitud_cancelacion, eliminar_solicitud_recursos_financieros, guardar_dictaminado, seleccion_usuarios, ver_administrador, ver_solicitudes_cambio, ver_solicitudes_cancelacion, ver_solicitudes_comite, registrar_administrador, eliminar_administrador, editar_administrador, inicio, ver_solicitudes_equivalencia, ver_solicitudes_movilidad, ver_solicitudes_recursos_financieros, ver_solicitudes_traslado

from aplicacionAlumnos.views import detalle_solicitud_alumno, inicio_alumno, alumno_equivalencia, mostrar_template_archivo, muestra_archivos_cambio, muestra_archivos_equivalencia, muestra_archivos_movilidad, muestra_archivos_peticion, muestra_archivos_traslado,  pdf_equivalencia, pdf, pdf_cambio, pdf_traslado, prueba_correo, registrar_alumno, solicitar_referencia, solicitud_cambio, solicitud_comite, pdf_comite, solicitud_traslado, ver_mis_solicitudes, detalle_alumno, cambiar_psw, recuperar_psw

urlpatterns = [

    # -------------------------- LOGIN / LOGOUT --------------------------  #
    path('adminn/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('accounts/login/',LoginView.as_view(template_name="html/login_administrador.html"), name="login"),
    path('logout/', logout_then_login, name='logout'),


    # -------------------------- ADMINSTRADORES --------------------------  #
    path('inicio_administrador/',login_required(ver_administrador), name='administrador'),
    path('administrador_usuarios/', login_required(administrar_usuarios), name='usuarios'),
    path('seleccion_usuarios/', seleccion_usuarios, name='seleccion_usuarios'),
    path('registrar_administrador/', login_required(registrar_administrador), name='registrar_administrador'),
    path('eliminar_administrador/<int:id_administrador>', login_required(eliminar_administrador), name="eliminar_administrador"),
    path('editar_administrador/<int:id_administrador>', login_required(editar_administrador), name="editar_administrador"),


    # ------------- SOLICITUDES -------------  #
    path('solicitudes_cambio/', login_required(ver_solicitudes_cambio), name='cambio'),
    path('solicitudes_comite/', login_required(ver_solicitudes_comite), name='comite'),
    path('solicitudes_cancelacion/', login_required(ver_solicitudes_cancelacion), name='cancelacion'),
    path('solicitud_movilidad/', login_required(ver_solicitudes_movilidad), name='movilidad'),
    path('solicitud_traslado/', login_required(ver_solicitudes_traslado), name='traslado'),
    path('solicitud_equivalencia/',login_required(ver_solicitudes_equivalencia), name='equivalencia'),
    path('solicitud_recursos_financieros/',login_required(ver_solicitudes_recursos_financieros), name='recursos_financieros'),
    path('eliminar_solicitud_recursos_financieros/<int:id_peticion>',login_required(eliminar_solicitud_recursos_financieros), name="eliminacion_solicitud_recursos_financieros"),
    path('detalle_solicitud/<int:id_solicitud>', login_required(detalle_solicitud), name="detalle_solicitud"),
    path('detalle_solicitud_cancelacion/<int:id_solicitud>', login_required(detalle_solicitud_cancelacion), name="detalle_solicitud_cancelacion"),

    path('mis_solicitudes/', ver_mis_solicitudes, name='ver_mis_solicitudes'),

    path('dictaminado/', guardar_dictaminado, name='guarda'),

    # -------------------------- ALUMNOS --------------------------  #
    path('login_alumno/',LoginView.as_view(template_name="login_alumno.html"), name="login_alumno"),
    path('inicio_alumno/', login_required(inicio_alumno), name='alumno'),
    path('registrar_alumno/', registrar_alumno, name="registrar_alumno"),
    path('detalle_solicitud_alumno/<int:id_alumno>',login_required(detalle_solicitud_alumno), name="detalle_solicitud_alumno"),
    path('detalle_alumno/<int:numero_control>', login_required(detalle_alumno), name='detalle_alumno'),
    path('cambiar_psw/<int:numero_control>', login_required(cambiar_psw), name='cambiar_psw'),
    path('recupera_psw/', recuperar_psw, name='recuperar_psw'),
    path('solicitar_referencia/<int:numero_control>', login_required(solicitar_referencia), name='solicitar_referencia'),
    


    # ------------- PDFS -------------  #
    path('alumno_equivalencia/', alumno_equivalencia, name="alumno_equivalencia"),
    path('pdf_equivalencia/', pdf_equivalencia, name="pdf_equivalencia"),
    path('pdf/', pdf, name="pdf"),
    path('pdfequivalencia/', login_required(pdf_equivalencia), name="pdf_equivalencia"),
    path('pdf_cambio', pdf_cambio, name = 'pdf_cambio' ),
    path('pdf_comite', pdf_comite, name='pdf_comite'),
    path('pdf_traslado', pdf_traslado, name = 'pdf_traslado'),


    # ------------- DRAG AND DROPS DE ARCHIVOS -------------  #
    path('archivos_cambio_carrera/', muestra_archivos_cambio, name='archivosCambio'),
    path('archivos_peticion/', muestra_archivos_peticion, name='archivosPeticion'),
    path('archivos_movilidad/', muestra_archivos_movilidad, name='archivosMovilidad'), 
    path('archivos_traslado/', muestra_archivos_traslado, name='archivosTraslado'), 
    path('archivos_equivalencia/', muestra_archivos_equivalencia, name='archivosEquivalencia'), 
    path('prueba_archivo/', mostrar_template_archivo, name='prueba'),

    path('prueba_correo', prueba_correo, name='pruebaCorreo'),
    # path('contacto/', correo, name='contact'),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]

# if settings.DEBUG:
#     urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 
    # path('solicitudes_participacion/', login_required(ver_solicitudes_participacion), name='participacion'),
    # path('solicitudes_convalidacion/', login_required(ver_solicitudes_convalidacion), name='convalidacion'),
    # path('solicitudes_resolucion/', login_required(ver_solicitudes_resolucion), name='resolucion'),

    # path('detalle_administrdaor/<int:id_administrador>', detalle_administrador, name="detalle_administrador"),
    #path('eliminar_administrador/<int:id_administrador>', eliminar_administrador, name="eliminar_administrador"),
    #path('editar_administrador/<int:id_administrador>', editar_administrador, name="editar_administrador"),