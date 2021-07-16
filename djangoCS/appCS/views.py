import mimetypes
import os
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora

# Create your views here.
def login(request):

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

            #Si la contraseña es igual...
            if pwd == contraReal:

                usuarioLogueado = True

                request.session['idSesion'] = id
                request.session['correoSesion'] = correo
                request.session['nombres'] = nombres
                request.session['apellidos'] = apellidos

                return redirect('/inicio/') #redirecciona a url de inicio

            #Si la contraseña esta mal..
            else:
                hayError = True
                error = "Ha ingresado mal la contraseña"
                return render(request, "Login/login.html", {"hayError": hayError, "textoError":error})

        #Si no se encuentra a nadie con ese correo...
        else:
            hayError = True
            error = "No se ha encontrado al usuario"
            return render(request, "Login/login.html", {"hayError":hayError, "textoError":error})

    #se carga la pagina por primera vez.
    return render(request, "Login/login.html")

def inicio(request):

    estaEnInicio = True

    return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio})

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

        
        estaEnAgregarCarta = True
        return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "compuSeleccionada":compuSeleccionada, "arreglo":arregloDatosCompu, "arregloEmpl": datosEmpleado})

    estaEnAgregarCarta = True
    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta})

def EmpleadosBitacora(request):
    estaEnEmpleadosBitacora = True
    return render(request, "Bitacora/Empleados.html",{"estaEnEmpleadosBitacora": estaEnEmpleadosBitacora})

def EquiposBitacora(request):
    estaEnEquiposBitacora = True
    return render(request, "Bitacora/Equipos.html",{"estaEnEquiposBitacora": estaEnEquiposBitacora})

def ImpresorasBitacora(request):
    estaEnImpresorasBitacora = True
    return render(request, "Bitacora/Impresoras.html",{"estaEnImpresorasBitacora": estaEnImpresorasBitacora})

def MantenimientoBitacora(request):
    estaEnMantenimientoBitacora = True
    return render(request, "Bitacora/Mantenimiento.html",{"estaEnMantenimientoBitacora": estaEnMantenimientoBitacora})

def CartuchosBitacora(request):
    estaEnCartuchosBitacora = True
    return render(request, "Bitacora/Cartuchos.html",{"estaEnCartuchosBitacora": estaEnCartuchosBitacora})

def CartasBitacora(request):
    estaEnCartasBitacora = True
    return render(request, "Bitacora/Cartas.html",{"estaEnCartasBitacora": estaEnCartasBitacora})

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