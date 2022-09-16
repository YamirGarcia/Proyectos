
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.where import AND
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.regex_helper import Group
from datetime import date

from aplicacionDB.models import Archivos, Documentos, Estudiante, Referencia, Solicitudes, Administrador

from aplicacionAdministrador.forms import AdministradorForm, SolicitudesForm, AlumnoForm

# Create your views here.

def inicio(request):    
    return redirect('login')

def seleccion_usuarios(request):
    user = request.user.groups.all()
    lista = list(user)
    if lista[0].name == 'Administrador' or lista[0].name == 'Administrador2':
        return redirect('administrador')
    if lista[0].name == 'Alumno':
        return redirect('alumno')
    if lista[0].name == 'Recursos Financieros':
        return redirect('recursos_financieros')
    else:
        return redirect('login')


def ver_administrador(request):
    return render(request,'html/inicio_administrador.html')
    
def ver_solicitudes_cambio(request): 
    filtro = Solicitudes.objects.filter(Q(tipoTramite=1)).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))

    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    estado = request.GET.get('estado')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if estado != '' and estado is not None:
        filtro = filtro.filter(estatusAdministrador=estado) 
        filters['estado'] = estado

    
    context = {
        'array_solicitudes': filtro,
        # 'ruta': ruta,
        # 'imagenRuta': imagen
    }
    # filtro.filter(estatusAdministrador=all).filter()
    return render(request, 'html/solicitudes_cambio_carrera.html', context)

def ver_solicitudes_comite(request):
    filtro = Solicitudes.objects.filter(Q(tipoTramite=2)).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))
    
    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    estado = request.GET.get('estado')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if estado != '' and estado is not None:
        filtro = filtro.filter(estatusAdministrador=estado) 
        filters['estado'] = estado

    context = {
        'array_solicitudes': filtro
    }
    return render(request, 'html/solicitudes_comite.html', context)


def ver_solicitudes_movilidad(request): 
    filtro = Solicitudes.objects.filter(tipoTramite=3).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))

    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    estado = request.GET.get('estado')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if estado != '' and estado is not None:
        filtro = filtro.filter(estatusAdministrador=estado) 
        filters['estado'] = estado

    
    context = {
        'array_solicitudes': filtro,
        # 'ruta': ruta,
        # 'imagenRuta': imagen
    }
    # filtro.filter(estatusAdministrador=all).filter()
    return render(request, 'html/solicitudes_movilidad.html', context)

def ver_solicitudes_traslado(request): 
    filtro = Solicitudes.objects.filter(tipoTramite=4).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))

    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    estado = request.GET.get('estado')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if estado != '' and estado is not None:
        filtro = filtro.filter(estatusAdministrador=estado) 
        filters['estado'] = estado

    
    context = {
        'array_solicitudes': filtro,
        # 'ruta': ruta,
        # 'imagenRuta': imagen
    }
    # filtro.filter(estatusAdministrador=all).filter()
    return render(request, 'html/solicitudes_traslado.html', context)


def ver_solicitudes_equivalencia(request): 
    filtro = Solicitudes.objects.filter(tipoTramite=5).exclude(Q(estatusAdministrador="Cancelado") | Q(estatusAdministrador="Cancelacion Pendiente"))

    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    estado = request.GET.get('estado')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if estado != '' and estado is not None:
        filtro = filtro.filter(estatusAdministrador=estado) 
        filters['estado'] = estado

    
    context = {
        'array_solicitudes': filtro,
        # 'ruta': ruta,
        # 'imagenRuta': imagen
    }
    # filtro.filter(estatusAdministrador=all).filter()
    return render(request, 'html/solicitudes_equivalencia.html', context)

def ver_solicitudes_cancelacion(request):
    filtro = Solicitudes.objects.filter(Q(estatusAlumno="Cancelacion Pendiente") | Q(estatusAlumno="Cancelado"))
    
    numeroControl = request.GET.get('no_control')
    folio = request.GET.get('folio')
    fechaCreacion =  request.GET.get('fechaCreacion')
    fechaCierre = request.GET.get('fechaCierre')
    carrera = request.GET.get('carrera')
    tipoTramite = request.GET.get('tipoTramite')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl__numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if folio != '' and folio is not None:
        filtro = filtro.filter(numeroFolio=folio)
        filters['folio'] = folio

    if fechaCreacion != '' and fechaCreacion is not None:
        filtro = filtro.filter(fechaCreacion=fechaCreacion) 
        filters['fechaCreacion'] = fechaCreacion

    if fechaCierre != '' and fechaCierre is not None:
        filtro = filtro.filter(fechaCierre = fechaCierre)     
        filters['fechaCierrre'] = fechaCierre
    
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(numeroControl__carrera=carrera)
        filters['carrera'] = carrera

    if tipoTramite != '' and tipoTramite is not None:
        filtro = filtro.filter(tipoTramite=tipoTramite) 
        filters['estado'] = tipoTramite

    context = {
        'array_solicitudes': filtro
    }
    return render(request, 'html/solicitudes_cancelacion.html', context)

def ver_solicitudes_recursos_financieros(request):
    filtro = Referencia.objects.all()
    numeroControl = request.GET.get('no_control')
    nombres = request.GET.get('nombres')
    carrera = request.GET.get('carrera')
    tipoTramite =  request.GET.get('tipoTramite')

    filters = {}

    if numeroControl != '' and numeroControl is not None:
        filtro = filtro.filter(numeroControl=numeroControl)
        filters['numeroControl'] = numeroControl

    if nombres != '' and nombres is not None:
        filtro = filtro.filter(nombres=nombres)
        filters['nombres'] = nombres
 
    if carrera != '' and carrera is not None:
        filtro = filtro.filter(carrera=carrera)
        filters['carrera'] = carrera

    if tipoTramite != '' and tipoTramite is not None:
        filtro = filtro.filter(tipoTramite=tipoTramite)
        filters['tipoTramite'] = tipoTramite
    
    context = {
        'solicitudes':filtro
    }
    return render(request, 'html/solicitudes_recursos_financieros.html', context)

def eliminar_solicitud_recursos_financieros(request, id_peticion):
    peticion =  get_object_or_404(Referencia, pk=id_peticion)
    print(peticion.id)
    print(peticion)

    if peticion:
        peticion.delete()
        messages.info(request, peticion.nombres)
    return redirect('recursos_financieros')


def detalle_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(Solicitudes, pk=id_solicitud)
    arrayArchivos = Archivos.objects.filter(numeroFolio = solicitud.id)
    # print(archivos)
    context={
        'solicitud':solicitud,
        'archivos': arrayArchivos
    }
    if request.method == "POST":
        estatusTemp = request.POST.get('estatus')
        if estatusTemp is None:
            estatusTemp = solicitud.estatusAdministrador

        # estatusNuevo = request.POST.get('estatus')
        solicitud.estatusAdministrador =  estatusTemp
        solicitud.estatusAlumno = estatusTemp
        if estatusTemp == 'Concluido':
            solicitud.fechaCierre = date.today()
        archivos = request.FILES.getlist('archivos')
        if archivos:
            for file in archivos:
                solicitud.dictamen = file
        
        solicitud.save()
        
    return render(request, 'html/detalle_solicitud.html', context)

def guardar_dictaminado(requet):
    if requet.method == 'POST':
        archivos = requet.FILES.getlist('archivos')
        print(archivos)
        return redirect('equivalencia')

def detalle_solicitud_cancelacion(request, id_solicitud):
    solicitud = get_object_or_404(Solicitudes, pk=id_solicitud)
    arrayArchivos = Archivos.objects.filter(numeroFolio = solicitud.id)
    context={
        'solicitud':solicitud,
        'archivos': arrayArchivos
    }
    if request.method == "POST":
        estatus = request.POST.get('opciones')
        if estatus == 'Cancelado':
            solicitud.estatusAdministrador =  estatus
            solicitud.estatusAlumno = estatus
            solicitud.fechaCierre = date.today()
        else:
            solicitud.estatusAdministrador =  estatus
            solicitud.estatusAlumno = estatus
        solicitud.save()
        
    return render(request, 'html/detalle_solicitud_cancelacion.html', context)


# def ver_solicitudes_participacion(request):
#     return render(request, 'html/solicitudes_participacion.html')

# def ver_solicitudes_convalidacion(request):
#     return render(request, 'html/solicitudes_convalidacion.html')

# def ver_solicitudes_resolucion(request):
#     return render(request, 'html/solicitudes_resolucion.html')






# ADMINISTRAR USUARIOS
def administrar_usuarios(request):
    adminUsuarios =  Administrador.objects.all()
    return render(request, 'html/administrador_usuarios.html', {'array_administradores':adminUsuarios})

def registrar_administrador(request):
    try:
        if request.method == 'POST':
            formaAdministrador = AdministradorForm(request.POST)
            user = User.objects.create_user(formaAdministrador['nombreUsuario'].value(),formaAdministrador['correo'].value(),formaAdministrador['contraseña'].value())
            if formaAdministrador.is_valid():
                if formaAdministrador['rangoAdministrador'].value() == 'SuperAdministrador':
                    user.groups.add(1)
                if formaAdministrador['rangoAdministrador'].value() == 'Administrador':
                    user.groups.add(3)
                else:
                    user.groups.add(4)
                user.save()
                user.refresh_from_db()
                formaAdministrador.save()
                return redirect('usuarios')
        else:
            formaAdministrador = AdministradorForm()
        context={
            'formaAdministrador':formaAdministrador,
        }
        return render(request, 'html/registrar_administrador.html', context)
    except:
        formaAdministrador = AdministradorForm()
        context={
            'formaAdministrador':formaAdministrador,
        }
        return render(request, 'html/registrar_administrador.html', context)
        


# def detalle_administrador(request, id_administrador):
#     administrador = get_object_or_404(Administrador, pk=id_administrador)
#     return render(request, 'html/detalle_administrador.html', {'administrador':administrador})

def eliminar_administrador(request, id_administrador):
    administrador = get_object_or_404(Administrador, pk=id_administrador)
    user = User.objects.get(username=administrador.nombreUsuario)
    if administrador:
        user.delete()
        administrador.delete()
    return redirect('usuarios')

def editar_administrador(request, id_administrador):
    administrador = get_object_or_404(Administrador, pk=id_administrador)
    # formaAdministrador = None
    if request.method == "POST":
        formaAdministrador = AdministradorForm(request.POST, instance=administrador)
        user = User.objects.get(username=administrador.nombreUsuario)
        user.delete()
        user = User.objects.create_user(formaAdministrador['nombreUsuario'].value(),formaAdministrador['correo'].value(),formaAdministrador['contraseña'].value())
        if formaAdministrador.is_valid():
            print(formaAdministrador['rangoAdministrador'].value())
            if formaAdministrador['rangoAdministrador'].value() == 'SuperAdministrador':
                user.groups.add(1)
            if formaAdministrador['rangoAdministrador'].value() == 'Administrador':
                user.groups.add(3)
            else:
                user.groups.add(4)
            user.save()
            user.refresh_from_db()
            formaAdministrador.save()
            return redirect('usuarios')
    else:
        formaAdministrador = AdministradorForm(instance=administrador)
    return render(request, 'html/detalle_administrador.html',{'formaAdministrador':formaAdministrador, 'admin': administrador})



# def register (request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             username  = form.cleaned_data['username']
#             messages.success(request, f'Usuario {username} cread')
#     else:
#         form = UserCreationForm()

#     context = {
#         'form': form
#     }
