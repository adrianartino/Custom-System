from django.shortcuts import render
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
                apellidos = dato.id_area
                puesto = dato.puesto
                correo = dato.correo
                contraReal = dato.constraseña
                activo = dato.activo

            #Si la contraseña es igual...
            if pwd == contraReal:

                usuarioLogueado = True

                request.session['idSesion'] = id
                request.session['correoSesion'] = correo
                request.session['nombres'] = nombres
                request.session['apellidos'] = apellidos

                return redirect('/inicio') #redirecciona a url de inicio

            #Si la contraseña esta mal..
            else:
                hayError = True
                error = "Ha ingresado mal la contraseña"
                return render(request, "Login/muestra.html", {"hayError": hayError, "textoError":error})

        #Si no se encuentra a nadie con ese correo...
        else:
            jajaja = 2

            




    #se carga la pagina por primera vez.
    return render(request, "Login/muestra.html")
    
