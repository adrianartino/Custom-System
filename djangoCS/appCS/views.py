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
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        estaEnInicio = True
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']

        #Si es la primera vez que inicia sesión.. Bienvenida 
        if "recienIniciado" in request.session:
            nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes

            del request.session['recienIniciado']

            recienIniciado = True
            
            return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo, "recienIniciado":recienIniciado, "nombre": nombre})

        #So no es la primera vez que inicia sesión
        nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes
        return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def verAreas(request):

    estaEnVerAreas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    
    nombreCompleto = nombre + " " + apellidos
    
    infoAreas = Areas.objects.all()

    return render(request, "Areas/verAreas.html", {"estaEnVerAreas":estaEnVerAreas, "nombreCompleto":nombreCompleto, "correo":correo, "listaAreas": infoAreas})

def agregarAreas(request):

    estaEnAgregarAreas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    
    nombreCompleto = nombre + " " + apellidos
    
    
            
    
    colores = [
                ["label bg-red", "radio_30", "with-gap radio-col-red", "Rojo"], #color.0 , color.1, color.2, color.3
                ["label bg-pink", "radio_31", "with-gap radio-col-pink", "Rosa"],
                ["label bg-purple", "radio_32", "with-gap radio-col-purple", "Morado"],
                ["label bg-indigo", "radio_33", "with-gap radio-col-indigo", "Indigo"],
                ["label bg-blue", "radio_34", "with-gap radio-col-blue", "Azul"],
                ["label bg-cyan", "radio_35", "with-gap radio-col-cyan", "Cyan"],
                ["label bg-teal", "radio_36", "with-gap radio-col-teal", "Aqua"],
                ["label bg-green", "radio_37", "with-gap radio-col-green", "Verde"],
                ["label bg-light-green", "radio_38", "with-gap radio-col-light-green", "Verde Bajo"],
                ["label bg-lime", "radio_39", "with-gap radio-col-lime", "Lima"],
                ["label bg-yellow", "radio_40", "with-gap radio-col-yellow", "Amarillo"],
                ["label bg-amber", "radio_41", "with-gap radio-col-amber", "Ambar"],
                ["label bg-orange", "radio_42", "with-gap radio-col-orange", "Naranja"],
                ["label bg-deep-orange", "radio_43", "with-gap radio-col-deep-orange", "Naranja Oscuro"],
                ["label bg-brown", "radio_44", "with-gap radio-col-brown", "Cafe"],
                ["label bg-grey", "radio_45", "with-gap radio-col-grey", "Gris"],
                ["label bg-blue-grey", "radio_46", "with-gap radio-col-blue-grey", "Gris Azulado"],
                ["label bg-black", "radio_47", "with-gap radio-col-black", "Negro"]
               ]
    
    nombresColores = ["Rojo", "Rosa", "Morado", "Indigo", "Azul", "Cyan", "Aqua", "Verde", "Verde bajo", "Verde Lima", "Amarillo", "Ambar", "Naranja", 
                      "Naranja Oscuro", "Cafe", "Gris", "Gris Azulado", "Negro"]
    
    #Obtener lista de colores en la table areas
    infoAreas = Areas.objects.all()
    
    coloresSi = []
    coloresNo = []
    
    for color in colores: 
        datosAreaCoincide = Areas.objects.filter(color__icontains=color[0])
        if datosAreaCoincide:
            coloresSi.append([color[0],color[1], color[2], color[3]] )
            
        else:
            coloresNo.append([color[0],color[1], color[2], color[3]])
            
    if request.method == "POST":
        area = request.POST['area']
        color = request.POST['colorElegido']
        
        
                
        areaExiste = Areas.objects.filter(nombre__icontains= area)
        if areaExiste:
            errorExiste= True
            mensajeError = "El área " + area + " ya existe en la base de datos"
            return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "arregloColores":colores, "nombresColores":nombresColores,
            "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, "error": errorExiste,
            "mensaje": mensajeError})
        else:
            
            registro = Areas(nombre=area, color=color)
            registro.save()
            guardadoExito = True
            mensajeExito = "El área " + area + " fue agregado exitosamente"
            return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "arregloColores":colores, "nombresColores":nombresColores,
            "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, "guardado": guardadoExito,
            "mensaje": mensajeExito})
            

    return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "arregloColores":colores, "nombresColores":nombresColores, "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo})

def verEmpleados(request):

    estaEnVerEmpleados = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    empleadosActivos = Empleados.objects.filter(activo__icontains= "A")
    empleadosInactivos = Empleados.objects.filter(activo__icontains= "I")
    
    #empleados Actvos
    areasEnActivos = []
    datosAreasEnActivos = []
    
    for empleado in empleadosActivos:
        areasEnActivos.append(empleado.id_area_id)
        #areasEnActivos = ["1"]
        
    for id in areasEnActivos:
        datosArea = Areas.objects.filter(id_area__icontains = id) #["1", "Sistemas", "rojo"]
        
        if datosArea:
            for dato in datosArea:
                nombreArea = dato.nombre
                colorArea = dato.color
        
        datosAreasEnActivos.append([nombreArea, colorArea])
        
    lista = zip(empleadosActivos, datosAreasEnActivos)
                
    
    #empleadosInactivos
    areasEnInactivos = []
    datosAreasEnInactivos = []
    
    for empleado in empleadosInactivos:
        areasEnInactivos.append(empleado.id_area_id)
        
    for id in areasEnInactivos:
        areasInactivos = Areas.objects.filter(id_area__contains = id)
            
        if areasInactivos:
            for dato in areasInactivos:
                nombreArea = dato.nombre
                colorArea = dato.color
                    
        datosAreasEnInactivos.append([nombreArea, colorArea])
            
    lista1 = zip (empleadosInactivos, datosAreasEnInactivos)
    
    
    if "idEmpleadoAlta" in request.session:
        alta = True
        mensaje = "Se dio de alta al empleado " + request.session['idEmpleadoAlta']
        del request.session["idEmpleadoAlta"]
        return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "alta":alta, "mensaje":mensaje})
    
    if "idEmpleadoBaja" in request.session:
        baja = True
        mensaje = "Se dio de baja al empleado " + request.session['idEmpleadoBaja']
        del request.session["idEmpleadoBaja"]
        return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "baja":baja, "mensaje":mensaje})
    
    return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1 })

def agregarEmpleados(request):

    estaEnAgregarEmpleados = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    info_areas = Areas.objects.only('id_area', 'nombre', 'color')

    if request.method == "POST":

        nombre_recibido = request.POST['nombreEm']
        apellido_recibido = request.POST['apellidoEm']
        area_recibida = request.POST['areaEm']
        puesto_recibido = request.POST['puestoEm']
        correo_recibido = request.POST['correoEm']
        contra_recibida = request.POST['contraEm']

        if request.POST.get('activoEm', False):
            activo_recibido = "A"
        elif request.POST.get('activoEm', True):
            activo_recibido = "I"

        lista_empleados = Empleados.objects.all()

        for empleado in lista_empleados:
            if empleado.apellidos == apellido_recibido and empleado.correo == correo_recibido:
                yaExiste = True
                texto_error = "El empleado "+ empleado.nombre + " ya existe en la Base de Datos!"
                return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "yaExiste":yaExiste, "textoError":texto_error})
            else:
                noExiste = True
                texto_existe = "El empleado "+ nombre_recibido + " fue agregado exitosamente!"
                registro = Empleados(nombre=nombre_recibido, apellidos=apellido_recibido, 
                id_area = Areas.objects.get(id_area = area_recibida), puesto=puesto_recibido, correo = correo_recibido, contraseña=contra_recibida, activo = activo_recibido )
                registro.save()
                return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "noExiste":noExiste, "textoExiste":texto_existe})

    return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas})

def verEquipos(request):

    estaEnVerEquipos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    equiposActivos = Equipos.objects.filter(activo__icontains= "A")
    equiposInactivos = Equipos.objects.filter(activo__icontains= "I")
    
     #empleados Actvos
    empleadosEnActivos = []
    datosAreasEnActivos = []
  
    
    for equipos in equiposActivos:
        empleadosEnActivos.append(equipos.id_empleado_id)
     
        #areasEnActivos = ["1"]
        
    for id in empleadosEnActivos:
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = id) #["1", "Sistemas", "rojo"]
        
        if datosEmpleado:
            for dato in datosEmpleado:
                nombreEmpleado = dato.nombre
                apellidosEmpleado = dato.apellidos
                areaEmpleado = dato.id_area_id
                datosArea = Areas.objects.filter(id_area__icontains=areaEmpleado)
                
                if datosArea:
                    for dato in datosArea:
                        nombreArea = dato.nombre
                        color = dato.color
        
        datosAreasEnActivos.append([nombreEmpleado, apellidosEmpleado, nombreArea, color])
        
    lista = zip(equiposActivos, datosAreasEnActivos)
    
         #empleados InActvos
    empleadosEnInactivos = []
    datosAreasEnInactivos = []
    
    
    for equipos in equiposInactivos:
        empleadosEnInactivos.append(equipos.id_empleado_id)
       
        #areasEnActivos = ["1"]
        
    for id in empleadosEnInactivos:
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = id) #["1", "Sistemas", "rojo"]
        
        if datosEmpleado:
            for dato in datosEmpleado:
                nombreEmpleado = dato.nombre
                apellidosEmpleado = dato.apellidos
                areaEmpleado = dato.id_area_id
                datosArea = Areas.objects.filter(id_area__icontains=areaEmpleado)
                
                if datosArea:
                    for dato in datosArea:
                        nombreArea = dato.nombre
                        color = dato.color
        
        datosAreasEnInactivos.append([nombreEmpleado, apellidosEmpleado, nombreArea, color])
        
    lista2 = zip(equiposInactivos, datosAreasEnInactivos)
    
    if "idEquipoBaja" in request.session:
        bajaEquipo=True
        bajaExito= "Se dió de baja el " + request.session["idEquipoBaja"] + " con éxito!"
        del request.session["idEquipoBaja"]
        return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "lista2":lista2, "bajaEquipo":
            bajaEquipo, "bajaExito": bajaExito})
        
    if "idEquipoAlta" in request.session:
        altaEquipo= True
        altaExito= "Se dió de alta el " + request.session["idEquipoAlta"] + " con éxito"
        del request.session["idEquipoAlta"]
        return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "lista2":lista2,
                                                           "altaEquipo": altaEquipo, "altaExito":altaExito})

    return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "lista2":lista2})

def agregarEquipos(request):

    estaEnAgregarEquipos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    info_empleados = Empleados.objects.only('id_empleado', 'nombre', 'apellidos')
    empleadosEquipo = Equipos.objects.only('id_empleado_id')
    empleadosiEq= []
    empleadosnoEq= []
    
    if empleadosEquipo:
    
        for empleados in info_empleados:
            for emplEq in empleadosEquipo:
                if empleados.id_empleado == emplEq.id_empleado_id:
                    empleadosiEq.append(empleados.id_empleado)
                else:
                    empleadosnoEq.append([empleados.id_empleado,empleados.nombre,empleados.apellidos])
                    
        return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo,"info_empleados":empleadosnoEq })
                

    
    if request.method == "POST":
    
        tipo_recibido = request.POST['tipo']
        marca_recibido = request.POST['marca']
        modelo_recibida = request.POST['modelo']
        color_recibido = request.POST['color']
        imagen_recibido = request.FILES.get('imgequipo')
        pdf_recibido = request.FILES.get('pdf')
        memoriaram_recibida = request.POST['memram']
        procesador_recibida = request.POST['procesador']
        sistemaop_recibida = request.POST['sisteop']
        estado_recibida = request.POST['estado']
        propietario_recibida = request.POST['propietario']

        if request.POST.get('activoEm', False):
            activo_recibido = "I"
        elif request.POST.get('activoEm', True):
            activo_recibido = "A"
            
        
        
            
        if propietario_recibida == "nopropietario":
            registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                              color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                              memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                              estado=estado_recibida, activo=activo_recibido)
            registroCompu.save()
            compuSin = True
            textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " sin propietario!"
            return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "compuSin": compuSin, "textoCompu":textoCompu})
            
            
        elif propietario_recibida != "nopropietario":
            infoEmpleado = Empleados.objects.filter(id_empleado__icontains=propietario_recibida)
            
            for dato in infoEmpleado:
                nombre = dato.nombre
                
            compuCon= True
            textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " asignada al empleado " + nombre +"!"
            registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                              color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                              memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                              id_empleado =Empleados.objects.get(id_empleado = propietario_recibida),estado=estado_recibida, activo=activo_recibido)
            registroCompu.save()
            return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "compuCon": compuCon, "textoCompu":textoCompu})
    
    return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo,"info_empleados": info_empleados})

def verImpresoras(request):

    estaEnVerImpresoras = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "nombreCompleto":nombreCompleto, "correo":correo})

def agregarImpresoras(request):

    estaEnAgregarImpresoras = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    info_areas = Areas.objects.only('id_area', 'nombre', 'color')
    if request.method == "POST":
        
        marca_recibido = request.POST['marcas']
        modelo_recibido = request.POST['modelos']
        numserie_recibida = request.POST['nserie']
        imagen_recibida = request.FILES.get('imgeimpresora')
        tipo_recibida = request.POST['tipos']
        areas_recibida = request.POST['areas']
        estados_recibida = request.POST['estados']
        
        if request.POST.get('red', False):
            red_recibido = "N"
        elif request.POST.get('red', True):
            red_recibido = "S"
            
        if request.POST.get('acin', False):
            activo_recibido = "I"
        elif request.POST.get('acin', True):
            activo_recibido = "A"
        
        ip_recibida = request.POST['ip']
        
        if ip_recibida == "":
            ip_recibida = "No ip"    
    
        registroImpresora=Impresoras(marca=marca_recibido, modelo= modelo_recibido,numserie=numserie_recibida,
                                     imagen=imagen_recibida, tipo=tipo_recibida,enred=red_recibido, 
                                     ip=ip_recibida, estado=estados_recibida, activo= activo_recibido,id_area = Areas.objects.get(id_area = areas_recibida))
        registroImpresora.save()
        impresoraAgregada = True
        
        impresoraExito= "La impresora " + marca_recibido + " " + modelo_recibido + " se guardó con éxito" 
        return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas,
                                                                    "impresoraAgregada":impresoraAgregada, "impresoraExito": impresoraExito})
         
    
            
    
            
        
    
    
    
    return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas})


def verInsumos(request):

    Insumos = True
    estaEnVerInsumos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos, "nombreCompleto":nombreCompleto, "correo":correo})

def agregarInsumos(request):

    estaEnAgregarInsumos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    Insumos = True
    return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos, "nombreCompleto":nombreCompleto, "correo":correo})

def verProgramas(request):

    estaEnVerProgramas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas, "nombreCompleto":nombreCompleto, "correo":correo})

def agregarProgramas(request):

    estaEnAgregarProgramas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas, "nombreCompleto":nombreCompleto, "correo":correo})

def asignarProgramas(request):

    estaEnAsignarProgramas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Programas/asignarProgramas.html",{"estaEnAsignarProgramas": estaEnAsignarProgramas, "nombreCompleto":nombreCompleto, "correo":correo})

def ProgramasporArea(request):

    estaEnverProgramasPorArea = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Programas/verProgramasArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "nombreCompleto":nombreCompleto, "correo":correo})

def verProgramasPorArea(request):
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    if request.method == "POST":
        
        nombreArea = request.POST['nombreArea']
        #nombreArea = Administracion

        estaEnverProgramasPorArea = True
        return render(request, "Programas/tablaProgArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "nombreArea":nombreArea, "nombreCompleto":nombreCompleto, "correo":correo})

    

def calendarioMant(request):

    estaEnCalendario = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request,"Mantenimiento/calendarioMant.html", {"estaEnCalendario": estaEnCalendario, "nombreCompleto":nombreCompleto, "correo":correo})

def formularioMant(request):
    estaEnFormulario = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "nombreCompleto":nombreCompleto, "correo":correo})

def verCarta(request):
    estaEnVerCarta = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request,"cartaCompromiso/verCarta.html", {"estaEnVerCarta": estaEnVerCarta, "nombreCompleto":nombreCompleto, "correo":correo})

def agregarCarta(request):
    
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

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
        return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "compuSeleccionada":compuSeleccionada, "arreglo":arregloDatosCompu, "arregloEmpl": datosEmpleado, "nombreCompleto":nombreCompleto, "correo":correo})

    estaEnAgregarCarta = True
    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasEquipos(request):
    estaEnEquiposBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEquiposBitacora": estaEnEquiposBitacora, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasImpresoras(request):
    estaEnImpresorasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnImpresorasBitacora": estaEnImpresorasBitacora, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasEmpleados(request):
    estaEnEmpleadosBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEmpleadosBitacora": estaEnEmpleadosBitacora, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasMantenimiento(request):
    estaEnMantenimientoBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnMantenimientoBitacora": estaEnMantenimientoBitacora, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasCartuchos(request):
    estaEnCartuchosBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnCartuchosBitacora": estaEnCartuchosBitacora, "nombreCompleto":nombreCompleto, "correo":correo})

def BitacorasCartas(request):
    estaEnCartasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    return render(request, "Bitacora/Bitacoras.html",{"estaEnCartasBitacora": estaEnCartasBitacora, "nombreCompleto":nombreCompleto, "correo":correo})



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
    estaEnCartasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        equipoRecibido = request.POST['idEquipo']
        datosEquipo = []





    return render(request, "Editar/editarEquipo.html", {"nombreCompleto":nombreCompleto, "correo":correo})


def editarEmpleado(request):
    estaEnCartasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    if request.method == "POST":
        
        empleadoRecibido = request.POST['idEmpleadoEditar']
        
        
        datosEmpleadoEditar = Empleados.objects.filter(id_empleado__icontains = empleadoRecibido)
        
        if datosEmpleadoEditar:
            for datoEditar in datosEmpleadoEditar:
            
                idareaEmpleado = datoEditar.id_area_id
                
        datosArea = Areas.objects.filter(id_area__icontains = idareaEmpleado)
        if datosArea:
            for nombreEditar in datosArea:
                
                nombreArea =  nombreEditar.nombre
        
        areas = Areas.objects.all()
        
        areasNuevas = []
        
        for dato in areas:
            if idareaEmpleado == dato.id_area:
                yaEsta = True
            else:
                areasNuevas.append([dato.id_area, dato.nombre])
                
        return render(request,"Editar/editarEmpleado.html", { "nombreCompleto":nombreCompleto, "correo":correo, "datosEmpleadoEditar": datosEmpleadoEditar, "nombreArea": nombreArea, "areasNuevas":areasNuevas})

def editarEmpleadoBd(request):
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        
        nombreEditar = request.POST['nombreEditar']
        apellidoEditar = request.POST['apellidoEditar']
        areaEditar = request.POST['areaEditar']
        puestoEditar = request.POST['puestoEditar']
        correoEditar = request.POST['correoEditar']
        contraseñaEditar = request.POST['contraseñaEditar']
        
        if request.POST.get('activoEditar', False):
            activoEditar = "A"
        elif request.POST.get('activoEditar', True):
            activoEditar = "I"
        
        
        
        areaInt = int(areaEditar)
        
        datosEmpleado = Empleados.objects.filter(correo__icontains = correoEditar)
        
        if datosEmpleado:
            for dato in datosEmpleado:
                idEmpleado = dato.id_empleado
        
        actualizacion = Empleados.objects.filter(correo__icontains = correoEditar).update(nombre=nombreEditar, apellidos=apellidoEditar,
                                                                                          id_area=areaInt, puesto=puestoEditar, 
                                                                                          correo=correoEditar, contraseña=contraseñaEditar, 
                                                                                          activo=activoEditar)
        
        
        editado = True
        textoEdicion = "Se ha editado al empleado " + nombreEditar + " con éxito!"
        
        datosEmpleadoEditar = Empleados.objects.filter(id_empleado__icontains = idEmpleado)
        
        if datosEmpleadoEditar:
            for datoEditar in datosEmpleadoEditar:
            
                idareaEmpleado = datoEditar.id_area_id
                
        datosArea = Areas.objects.filter(id_area__icontains = idareaEmpleado)
        if datosArea:
            for nombreEditar in datosArea:
                
                nombreArea =  nombreEditar.nombre
        
        areas = Areas.objects.all()
        
        areasNuevas = []
        
        for dato in areas:
            if idareaEmpleado == dato.id_area:
                yaEsta = True
            else:
                areasNuevas.append([dato.id_area, dato.nombre])
                
        return render(request,"Editar/editarEmpleado.html", { "nombreCompleto":nombreCompleto, "correo":correo, "datosEmpleadoEditar": datosEmpleadoEditar, "nombreArea": nombreArea, "areasNuevas":areasNuevas, "editado":editado, "textoEdicion":textoEdicion, "areaEditar":areaEditar})
    
def altaEmpleado(request):
    
    if request.method == "POST":
    
        idAlta= request.POST['idEmpleadoAlta']
        
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = idAlta)
        
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellido = dato.apellidos
            
        nombreCompletoEmp = nombre + " " + apellido
        
        actualizacion = Empleados.objects.filter(id_empleado__icontains = idAlta).update(activo = "A")
        
        
        request.session['idEmpleadoAlta'] = nombreCompletoEmp
        
        return redirect('/verEmpleados/')
    
def bajaEmpleado(request):
    
    if request.method == "POST":
    
        idBaja= request.POST['idEmpleadoBaja']
        
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = idBaja)
        
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellido = dato.apellidos
        
        nombreCompletoEmp = nombre + " " + apellido
        
        actualizacion = Empleados.objects.filter(id_empleado__icontains = idBaja).update(activo = "I")
        
        request.session['idEmpleadoBaja'] = nombreCompletoEmp
        
        return redirect('/verEmpleados/')
    
    
def altaEquipo(request):
    
    if request.method == "POST":
        
        idAlta= request.POST['idEquipoAlta']
        
        datosEquipo = Equipos.objects.filter(id_equipo__icontains = idAlta)
        
        for dato in datosEquipo:
            marca = dato.marca
            modelo = dato.modelo
        
        equipo = marca + " " + modelo
        
        actualizacion = Equipos.objects.filter(id_equipo__icontains = idAlta).update(activo = "A")
        
        request.session['idEquipoAlta'] = equipo
        
    
        return redirect('/verEquipos/')
        
  
def bajaEquipo(request):
    
    if request.method == "POST":
        
        idBaja= request.POST['idEquipoBaja']
        
        datosEquipo = Equipos.objects.filter(id_equipo__icontains = idBaja)
        
        for dato in datosEquipo:
            marca = dato.marca
            modelo = dato.modelo
        
        equipo = marca + " " + modelo
        
        actualizacion = Equipos.objects.filter(id_equipo__icontains = idBaja).update(activo = "I")
        
        request.session['idEquipoBaja'] = equipo
        
    
        return redirect('/verEquipos/')
        

def editarImpresora(request):
    estaEnCartasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    if request.method == "POST":

        idImpresora= request.POST['idImpresoraEditar']
        datosImpresora = [idImpresora, "HP", "SAD34", "345SFSEA", "Inyección de tinta Color/Blanco-Negro", "si", "192.164.2.10", "Funcional", "A", "Administración"]

        return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datosImpresora, "nombreCompleto":nombreCompleto, "correo":correo})

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

    