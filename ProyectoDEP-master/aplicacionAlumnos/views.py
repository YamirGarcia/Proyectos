from re import template
from typing import ContextManager
from warnings import catch_warnings
from django.db import models
from django.db.models import Q
from django.db.models.sql.where import AND
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views import View

from aplicacionDB.models import Archivos, Estudiante, Solicitudes, Tramites, Referencia
from aplicacionAlumnos.forms import AlumnoForm, DocumentoForm

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, response

#from weasyprint import HTML
from django.template.loader import get_template
from weasyprint import HTML

#fecha
from datetime import date
from datetime import datetime
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def inicio_alumno(request):
      return render(request, 'inicio_alumno.html')

def registrar_alumno(request):
      try: 
            if request.method == 'POST':
                  formaAlumno = AlumnoForm(request.POST)
                  user = User.objects.create_user(formaAlumno['numeroControl'].value(),formaAlumno['correo'].value(),formaAlumno['contraseña'].value())
                  if formaAlumno.is_valid():
                        user.groups.add(2)
                        user.save()
                        user.refresh_from_db()
                        formaAlumno.save()
                        return redirect('login')
            else:
                  formaAlumno = AlumnoForm()
            context={
                  'formaAlumno':formaAlumno,
            }
            return render(request, 'registrar_alumno.html', context)
      except:
          return redirect('login')

def pdf_equivalencia(request):
      fechaSF = datetime.now()
      fecha = f"{fechaSF.day}-{fechaSF.month}-{fechaSF.year}"
      papellido = request.POST.get('primerapellido')
      sapellido = request.POST.get('segundoapellido')
      nombre =  request.POST.get('nombre')
      calle = request.POST.get('calle')
      numero = request.POST.get('numero')
      col = request.POST.get('col')
      cp = request.POST.get('cp')
      municipio = request.POST.get('municipio')
      ciudad = request.POST.get('ciudad')
      estado = request.POST.get('estado')
      tel = request.POST.get('tel')
      nacio = request.POST.get('nacio')
      sexo = request.POST.get('sexo')
      inst = request.POST.get('inst')
      nivel = request.POST.get('nivel')
      area = request.POST.get('area')
      estadorep = request.POST.get('estadorep')
      carrera = request.POST.get('carrera')
      plan = request.POST.get('plan')
      fechai = request.POST.get('fechai')
      fechaf = request.POST.get('fechaf')
      instituto = request.POST.get('instituto')
      edorep = request.POST.get('edorep')
      tipocar = request.POST.get('tipocar')
      carreras = request.POST.get('carreras')
      planes = request.POST.get('planes')
      cel = request.POST.get('cel')
      correo = request.POST.get('correo')
      template = get_template('formatos/PDFequivalencia.html')
      context = {
            'fecha': fecha,
            'nombre': nombre,
            'papellido': papellido,
            'sapellido' : sapellido,
            'calle': calle,
            'numero': numero,
            'col': col,
            'cp' : cp,
            'municipio':municipio,
            'ciudad':ciudad,
            'estado':estado,
            'tel':tel,
            'nacio': nacio,
            'sexo':sexo,
            'inst': inst,
            'nivel':nivel,
            'area': area,
            'estadorep': estadorep,
            'carrera': carrera,
            'plan': plan,
            'fechai': fechai,
            'fechaf': fechaf,
            'instituto': instituto,
            'edorep': edorep,
            'tipocar': tipocar,
            'carreras': carreras,
            'planes': planes,
            'cel': cel,
            'correo': correo            
                  }
      html_template = template.render(context)
      pdf = HTML(string=html_template, base_url=request.build_absolute_uri(),).write_pdf()
      return HttpResponse(pdf, content_type='application/pdf')


def alumno_equivalencia (request):
      return render(request,'solicitud_equivalencia.html')


def pdf (request):
      return render(request, 'formatos/PDFequivalencia.html')


def solicitud_cambio(request):
      return render(request, 'solicitud_cambio.html')

# -------------- PESTAÑAS PARA SUBIR ARCHIVOS EN ALUMNOS -------------- #
# 1 - Cambio de Carrera
# 2 - Traslado (Comite)
# 3 - Movilidad
# 4 - Traslado
# 5 - Equivalencia
# 6 - Cancelacion 

def generar_folio(base):
      numero = str(random.randint(1, 5000))
      base += numero
      identificador = format(id(base), 'x')
      print(identificador.upper())
      return identificador.upper()

# 1 - CAMBIO DE CARRERRA
def muestra_archivos_cambio(request):
      context = {
            # "fecha": request.session['numeroControl']
      }
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            if listaArchivos:

                  correoAlumno = request.user.email
                  folio = generar_folio(request.user.email)

                  alumno = Estudiante.objects.get(correo=correoAlumno)
                  tramiteCambio = Tramites.objects.get(id=1)
                  
                  if alumno:

                        Solicitudes(numeroControl = alumno, 
                        numeroFolio=folio, 
                        estatusAlumno='Pendiente', 
                        estatusAdministrador='Pendiente', 
                        fechaCreacion=date.today(), 
                        tipoTramite =tramiteCambio).save()

                  solicitud = Solicitudes.objects.get(numeroFolio=folio)
                  for archivo in listaArchivos:
                        Archivos(documento=archivo, numeroFolio=solicitud).save()
                  request.session['guardado'] = 1
                  return render(request, 'archivos_cambio_carrera.html', context)
            else:
                  messages.info(request, 'Archivos vacios')
                  return render(request, 'archivos_cambio_carrera.html', context)

      if 'guardado' in request.session:
            del request.session['guardado']
      return render(request, 'archivos_cambio_carrera.html', context)

# 2 - PETICION A COMITÉ 
def muestra_archivos_peticion(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            if listaArchivos:
                  correoAlumno = request.user.email
                  folio = generar_folio(request.user.email)

                  alumno = Estudiante.objects.get(correo=correoAlumno)
                  tramiteCambio = Tramites.objects.get(id=2)
                  
                  if alumno:

                        Solicitudes(numeroControl = alumno, 
                        numeroFolio=folio, 
                        estatusAlumno='Pendiente', 
                        estatusAdministrador='Pendiente', 
                        fechaCreacion=date.today(), 
                        tipoTramite =tramiteCambio).save()

                  solicitud = Solicitudes.objects.get(numeroFolio=folio)
                  for archivo in listaArchivos:
                        Archivos(documento=archivo, numeroFolio=solicitud).save()
                  request.session['guardado'] = 1
                  return render(request, 'archivos_peticion.html')
            else:
                 messages.info(request, 'Archivos vacios')
                 return render(request, 'archivos_peticion.html') 

      if 'guardado' in request.session:
            del request.session['guardado']
      return render(request, 'archivos_peticion.html')

# 3 - MOVILIDAD
def muestra_archivos_movilidad(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            if listaArchivos:
                  correoAlumno = request.user.email
                  folio = generar_folio(request.user.email)

                  alumno = Estudiante.objects.get(correo=correoAlumno)
                  tramiteCambio = Tramites.objects.get(id=3)
                  
                  if alumno:

                        Solicitudes(numeroControl = alumno, 
                        numeroFolio=folio, 
                        estatusAlumno='Pendiente', 
                        estatusAdministrador='Pendiente', 
                        fechaCreacion=date.today(), 
                        tipoTramite =tramiteCambio).save()

                  solicitud = Solicitudes.objects.get(numeroFolio=folio)
                  for archivo in listaArchivos:
                        Archivos(documento=archivo, numeroFolio=solicitud).save()
                  request.session['guardado'] = 1
                  return render(request, 'archivos_movilidad.html')
            else:
                  messages.info(request, 'Archivos vacios')
                  return render(request, 'archivos_movilidad.html') 

      if 'guardado' in request.session:
            del request.session['guardado']

      return render(request, 'archivos_movilidad.html')

# 4 - TRASLADO
def muestra_archivos_traslado(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            if listaArchivos:
                  correoAlumno = request.user.email
                  folio = generar_folio(request.user.email)

                  alumno = Estudiante.objects.get(correo=correoAlumno)
                  tramiteCambio = Tramites.objects.get(id=4)
                  
                  if alumno:

                        Solicitudes(numeroControl = alumno, 
                        numeroFolio=folio, 
                        estatusAlumno='Pendiente', 
                        estatusAdministrador='Pendiente', 
                        fechaCreacion=date.today(), 
                        tipoTramite =tramiteCambio).save()

                  solicitud = Solicitudes.objects.get(numeroFolio=folio)
                  for archivo in listaArchivos:
                        Archivos(documento=archivo, numeroFolio=solicitud).save()
                  request.session['guardado'] = 1
                  return render(request, 'archivos_traslado.html')
            else:
                  messages.info(request, 'Archivos vacios')
                  return render(request, 'archivos_traslado.html') 

      if 'guardado' in request.session:
            del request.session['guardado']

      return render(request, 'archivos_traslado.html')

# 5 - EQUIVALENCIA
def muestra_archivos_equivalencia(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            if listaArchivos:

                  correoAlumno = request.user.email
                  folio = generar_folio(request.user.email)

                  alumno = Estudiante.objects.get(correo=correoAlumno)
                  tramiteCambio = Tramites.objects.get(id=5)
                  
                  if alumno:

                        Solicitudes(numeroControl = alumno, 
                        numeroFolio=folio, 
                        estatusAlumno='Pendiente', 
                        estatusAdministrador='Pendiente', 
                        fechaCreacion=date.today(), 
                        tipoTramite =tramiteCambio).save()

                  solicitud = Solicitudes.objects.get(numeroFolio=folio)
                  for archivo in listaArchivos:
                        Archivos(documento=archivo, numeroFolio=solicitud).save()
                  request.session['guardado'] = 1
                  return render(request, 'archivos_equivalencia.html')
            else:
                  messages.info(request, 'Archivos vacios')
                  return render(request, 'archivos_equivalencia.html')
      if 'guardado' in request.session:
            del request.session['guardado']
      
      return render(request, 'archivos_equivalencia.html')
# -------------- -------------- #
def subir_archivos(request):
      return HttpResponse('subimos')


def pdf_cambio(request):
      
      template = get_template('formatos/PDFcambiocarrera.html')
      html_template = template.render(request.POST)
      pdf = HTML(string=html_template, base_url=request.build_absolute_uri(),).write_pdf()
      return HttpResponse(pdf, content_type='application/pdf')





def solicitud_comite(request):
      return render(request, 'solicitud_comite.html')

def   pdf_comite(request):
      template = get_template('formatos/PDFcomite.html')
      datos = request.POST
      html_template = template.render(datos)
      pdf = HTML(string=html_template, base_url=request.build_absolute_uri(),).write_pdf()
      return HttpResponse(pdf, content_type='application/pdf')



def solicitud_traslado(request):
      return render(request, 'solicitud_traslado.html')

def pdf_traslado(request):
      template = get_template('formatos/PDFtraslado.html')
      datos = request.POST
      html_template = template.render(datos)
      pdf = HTML(string=html_template, base_url=request.build_absolute_uri(),).write_pdf()
      return HttpResponse(pdf, content_type='application/pdf')
# DocumentosForm = modelform_factory(Documentos, exclude=['archivo'])

def mostrar_template_archivo(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            print(listaArchivos)
            folio = request.POST.get('numeroFolio')
            solicitud = Solicitudes.objects.get(id=folio)
            for archivo in listaArchivos:
                  Archivos(documento=archivo, numeroFolio=solicitud).save()

      context = {
            
      }
      return render(request, 'formatos/pruebas_archivos.html', context)

def ver_mis_solicitudes(request):
      user = request.user
      filtro = Solicitudes.objects.filter(numeroControl__numeroControl = user.username)
      context = {
            'array_solicitudes': filtro
      }
      return render(request, 'mis_solicitudes.html', context)

def detalle_solicitud_alumno(request, id_alumno):
      solicitud = get_object_or_404(Solicitudes, pk=id_alumno)
      arrayArchivos = Archivos.objects.filter(numeroFolio = solicitud.id)
      context = {
            'solicitud':solicitud,
            'archivos':arrayArchivos
      }
      if request.method == "POST":
            comentario = request.POST.get('comentario')
            solicitud.estatusAdministrador = 'Cancelacion Pendiente'
            solicitud.estatusAlumno = 'Cancelacion Pendiente'
            solicitud.comentarios = comentario
            solicitud.save()
            request.session['guardado'] = 1
            messages.info(request, 'Guardado')

      if 'guardado' in request.session:
            del request.session['guardado']
      
      return render(request, 'detalle_solicitud_alumno.html',context)

def archivos_cambio(request):
      if request.method == 'POST':
            listaArchivos = request.FILES.getlist('archivos')
            folio = request.POST.get('numeroFolio')
            solicitud = Solicitudes.objects.get(id=folio)
            for archivo in listaArchivos:
                  Archivos(documento=archivo, numeroFolio=solicitud).save()
      context = {

      }
      return render(request, 'cambio_archivos.html', context )

def solicitar_referencia(request, numero_control):
      id = Estudiante.objects.only('id').get(numeroControl=numero_control).id
      peticion = get_object_or_404(Estudiante, pk=id)
      if request.method == 'POST':
            print("Estudiante")
            referencia = Referencia(
                  numeroControl = peticion.numeroControl,
                  nombres = peticion.nombres+ " " + peticion.apellidoPaterno + " " + peticion.apellidoPaterno,
                  correo = peticion.correo,
                  carrera = peticion.carrera,
                  tipoTramite =  request.POST.get('tipoTramite')
            ).save()
      if request.POST.get('tipoTramite') == "Cambio de Carrera": 
            return redirect('archivosCambio')
      if request.POST.get('tipoTramite') == "Equivalencia": 
            return redirect('archivosEquivalencia')
      if request.POST.get('tipoTramite') == "Movilidad": 
            return redirect('archivosMovilidad')
      else:
            return redirect('alumno')
     

# def correo(request):
      # pass

def prueba_correo(request):
      if request.method == 'POST':
            nombre = request.POST['nombre']
            email = request.POST['correo']
            asunto = request.POST['asunto']
            mensaje = request.POST['mensaje']

            template = render_to_string('email_template.html', {
                  'name': nombre,
                  'email': email,
                  'message': mensaje
            })

            email = EmailMessage(
                  asunto,
                  template,
                  settings.EMAIL_HOST_USER,
                  [email]
            )

            email.fail_silently = False
            email.send()

            messages.success(request, 'Se ha enviado tu correo.')
            return redirect('pruebaCorreo')

      return render(request, 'prueba_correo.html')




def detalle_alumno(request, numero_control):
      id = Estudiante.objects.only('id').get(numeroControl=numero_control).id
      estudiante = get_object_or_404(Estudiante, pk=id)
      if request.method == "POST":
            print('hola')
            formaAlumno = AlumnoForm(request.POST, instance=estudiante)
            if formaAlumno.is_valid():
                  print('holax2')
                  formaAlumno.save()
                  return redirect('alumno')                  
      else:
            formaAlumno = AlumnoForm(instance=estudiante)
      return render(request, 'editar_alumno.html', {'formaAlumno':formaAlumno, 'admin':estudiante})


def cambiar_psw(request, numero_control):
      id = Estudiante.objects.only('id').get(numeroControl=numero_control).id
      estudiante = get_object_or_404(Estudiante, pk=id)
      user = User.objects.get(username=estudiante.numeroControl)
      contra = request.POST.get('psw')
      user.set_password(contra)
      user.save()
      user.refresh_from_db()
      return redirect('logout')

def recuperar_psw(request):
      try:
            numero1 = str(random.randint(1, 100000))
            contraseña = format(id(numero1), 'x')
            numeroControl = request.POST.get('numeroControl')
            ide = Estudiante.objects.only('id').get(numeroControl=numeroControl).id
            estudiante = get_object_or_404(Estudiante, pk=ide)
            correo = estudiante.correo
            user = User.objects.get(username=numeroControl)
            user.delete()
            user = User.objects.create_user(numeroControl,correo,contraseña)
            user.groups.add(2)
            asunto = "Recuperación de contraseña"
            mensaje = "Su contraseña se ha restablecido \nSu nueva copntraseña es: "+contraseña
            template = render_to_string('email_template.html', {
                        'name': numeroControl,
                        'email': correo,
                        'message': mensaje
                  })

            email = EmailMessage(
                        asunto,
                        template,
                        settings.EMAIL_HOST_USER,
                        [correo]
                  )

            email.fail_silently = False
            email.send()
            user.save()
            user.refresh_from_db()
            messages.success(request, 'Se ha enviado tu correo.')
            return redirect('login')
      except:
            return redirect('login')
      