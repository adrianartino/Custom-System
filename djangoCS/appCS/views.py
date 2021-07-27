import mimetypes
import os
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora
import base64
from django.core.files.base import ContentFile

# Create your views here.
def login(request):

    #Si ya existe una sesión
    if "idSesion" in request.session:
      return redirect('/inicio/')

    #Si no hay una sesión iniciada
    else:

        #si se apretó el botón.
        if request.method == "POST":
            
            correousuario = request.POST['username']
            pwd = request.POST['pass']

            datosUsuario = Empleados.objects.filter(correo__icontains=correousuario)

            #Si encontro a un usuario con ese correo...
            if datosUsuario:

                for dato in datosUsuario:
                    id = dato.id_empleado
                    nombres = dato.nombre
                    apellidos = dato.apellidos
                    puesto = dato.puesto
                    correo = dato.correo
                    contraReal = dato.contraseña
                    activo = dato.activo
                    area = dato.id_area

                #Si la contraseña es igual...
                if correousuario == correo and pwd == contraReal :

                    usuarioLogueado = True #Para indicar que el usuario entro al sistema..

                    request.session['idSesion'] = id
                    request.session['correoSesion'] = correo
                    request.session['nombres'] = nombres
                    request.session['apellidos'] = apellidos
                    request.session['recienIniciado'] = "primerInicio"

                    return redirect('/inicio/') #redirecciona a url de inicio

                #Si el correo está mal..
                elif correousuario != correo :
                    hayError = True
                    error = "No se ha encontrado al usuario"
                    return render(request, "Login/login.html", {"hayError": hayError, "textoError":error})

                #Si la contraseña está mal..
                elif pwd != contraReal:
                    hayError = True
                    usuarioEncontrado = True
                    error = "La contraseña está mal"
                    return render(request, "Login/login.html", {"hayError": hayError, "textoError":error, "correo":correo, "usuarioEncontrado":usuarioEncontrado})

            #Si no se encuentra a nadie con ese correo...
            else:
                hayError = True
                error = "No se ha encontrado al usuario"
                return render(request, "Login/login.html", {"hayError":hayError, "textoError":error})

        #se carga la pagina por primera vez.
        return render(request, "Login/login.html")

def salir(request):

   del request.session["idSesion"]
   del request.session['correoSesion']
   del request.session['nombres'] 
   del request.session['apellidos'] 

   return redirect('/login/')

def inicio(request):

    estaEnInicio = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']

    #Si es la primera vez que inicia sesión..
    if "recienIniciado" in request.session:
        nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes

        del request.session['recienIniciado']

        recienIniciado = True


        return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo, "recienIniciado":recienIniciado, "nombre": nombre})

    nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes


    return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo})

def verAreas(request):

    estaEnVerAreas = True

    return render(request, "Areas/verAreas.html", {"estaEnVerAreas":estaEnVerAreas})

def agregarAreas(request):

    estaEnAgregarAreas = True

    return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas})

def verEmpleados(request):

    estaEnVerEmpleados = True
            
    return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados})

def agregarEmpleados(request):

    estaEnAgregarEmpleados = True

    return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados})

def verEquipos(request):

    estaEnVerEquipos = True

    return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos})

def agregarEquipos(request):

    estaEnAgregarEquipos = True

    return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos})

def verImpresoras(request):

    estaEnVerImpresoras = True

    return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras})

def agregarImpresoras(request):

    estaEnAgregarImpresoras = True
    return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras})

def verInsumos(request):

    Insumos = True
    estaEnVerInsumos = True
    return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos})

def agregarInsumos(request):

    estaEnAgregarInsumos = True
    Insumos = True
    return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos})

def verProgramas(request):

    estaEnVerProgramas = True

    return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas})

def agregarProgramas(request):

    estaEnAgregarProgramas = True

    return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas})

def asignarProgramas(request):

    estaEnAsignarProgramas = True

    return render(request,"Programas/asignarProgramas.html",{"estaEnAsignarProgramas": estaEnAsignarProgramas})

def ProgramasporArea(request):

    estaEnverProgramasPorArea = True

    return render(request,"Programas/verProgramasArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea})

def verProgramasPorArea(request):

    if request.method == "POST":
        
        nombreArea = request.POST['nombreArea']
        #nombreArea = Administracion

        estaEnverProgramasPorArea = True
        return render(request, "Programas/tablaProgArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "nombreArea":nombreArea})

    

def calendarioMant(request):

    estaEnCalendario = True
    return render(request,"Mantenimiento/calendarioMant.html", {"estaEnCalendario": estaEnCalendario})

def formularioMant(request):
    estaEnFormulario = True

    return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario})

def verCarta(request):
    estaEnVerCarta = True
    return render(request,"cartaCompromiso/verCarta.html", {"estaEnVerCarta": estaEnVerCarta})

def agregarCarta(request):

    if request.method == "POST":
        
        compuSeleccionada = request.POST['compuSeleccionada']
        empleSeleccionado = request.POST['empleadoSeleccionado']

       

        arregloEmpleado = empleSeleccionado.split(' ')
        #[0] - Monica
        #[1] - Arriaga
        #[2] - Administracion

        datosEmpleado = ["2",	"Mónica",	"Arriaga",	"Administración	", "Recursos humanos", 	"rhumanos@customco.com.mx", 	"recursosh098","A"	]

        #compuSeleccionada = Laptop Lenovo ThinkPad

        arreglitoCompu = compuSeleccionada.split(' ')
        #[0] - Laptop
        #[1] - Lenovo
        #[2] - Pavilion 087

        #hACER Consulta en tabla de equipos.

        arregloDatosCompu = ["1", "Laptop", "HP", "Pavillion 087", "Negro",	"8 GB", "Intel Core i7", "Windows 10 Home 64 bits", "Blanca Gaeta",	"Sistemas",	"Funcional"	, "A"]

        request.session['datosCompu'] = arregloDatosCompu
        request.session['datosEmpleado'] = datosEmpleado

        #Guardar datos en la tabla Carta de la base de datos

        estaEnAgregarCarta = True
        return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "compuSeleccionada":compuSeleccionada, "arreglo":arregloDatosCompu, "arregloEmpl": datosEmpleado})

    estaEnAgregarCarta = True
    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta})

def BitacorasEquipos(request):
    estaEnEquiposBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEquiposBitacora": estaEnEquiposBitacora})

def BitacorasImpresoras(request):
    estaEnImpresorasBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnImpresorasBitacora": estaEnImpresorasBitacora})

def BitacorasEmpleados(request):
    estaEnEmpleadosBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEmpleadosBitacora": estaEnEmpleadosBitacora})

def BitacorasMantenimiento(request):
    estaEnMantenimientoBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnMantenimientoBitacora": estaEnMantenimientoBitacora})

def BitacorasCartuchos(request):
    estaEnCartuchosBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnCartuchosBitacora": estaEnCartuchosBitacora})

def BitacorasCartas(request):
    estaEnCartasBitacora = True
    return render(request, "Bitacora/Bitacoras.html",{"estaEnCartasBitacora": estaEnCartasBitacora})



def descargarPDF(request):

     if request.method == "POST":
        
        idEquipo = request.POST['idEquipo']

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        nombreArchivo = idEquipo+".pdf"
        ubicacionArchivo = BASE_DIR + '/media/pdfequipos/'+ nombreArchivo

        path = open(ubicacionArchivo, 'rb')

        mime_type, _= mimetypes.guess_type(ubicacionArchivo)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
        return response

        #return render(request, "Equipos/equipo.html", {"idEquipo":BASE_DIR})

def guardarImagen(request):
    estaEnAgregarCarta = True

    if request.method == "POST":
        
        canvasLargo = request.POST['canvasData']
        format, imgstr = canvasLargo.split(';base64,')
        ext = format.split('/')[-1]
        archivo = ContentFile(base64.b64decode(imgstr), name= 'canvas.' + ext)

    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta})

def editarEquipo(request):
    
    if request.method == "POST":
        equipoRecibido = request.POST['idEquipo']
        datosEquipo = []





    return render(request, "Editar/editarEquipo.html")


def editarEmpleado(request):

    if request.method == "POST":

        empleadoRecibido = request.POST['idEmpleadoEditar']

        datosEmpleado = ["3","Ana", "Gutierrez", "5", "Subdirectora", "anda.gutierrez@customco.com.mx", "anaGut674#", "A"]

        idArea = datosEmpleado[3]
        nombreArea = "Almacen"



        return render(request,"Editar/editarEmpleado.html", {"arregloDatos":datosEmpleado, "nombreArea":nombreArea})

def editarImpresora(request):

    if request.method == "POST":

        idImpresora= request.POST['idImpresoraEditar']
        datosImpresora = [idImpresora, "HP", "SAD34", "345SFSEA", "Inyección de tinta Color/Blanco-Negro", "si", "192.164.2.10", "Funcional", "A", "Administración"]

        return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datosImpresora})

def firmarCarta(request):

    #Hacer consulta al ultimo registro de la tabla de cartas, para ver la ultima carta preguardada.
    datosCarta = ["1", "2", "1", "23/07/2021"]
    idEmpleado = datosCarta[1] # id 2 que corresponde a monica
    idEquipo = datosCarta[2] # id 1 que corresponde a laptop hp

    #Consulta a la tabla de empleado.
    datosEmpleado = ["2",	"Mónica",	"Arriaga",	"Administración	", "Recursos humanos", 	"rhumanos@customco.com.mx", 	"recursosh098","A"	]
    #Consulta a la tabla equipo
    arregloDatosCompu = ["1", "Laptop", "HP", "Pavillion 087", "Negro",	"8 GB", "Intel Core i7", "Windows 10 Home 64 bits", "Blanca Gaeta",	"Sistemas",	"Funcional"	, "A"]

    return render(request, "cartaCompromiso/firmarCarta.html", { "arreglo":arregloDatosCompu, "arregloEmpl": datosEmpleado}) 

    