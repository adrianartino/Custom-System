import mimetypes
import os
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras
import base64
from django.core.files.base import ContentFile
from datetime import date, datetime
from datetime import timedelta
from calendar import calendar
from dateutil.relativedelta import relativedelta
from django.conf import settings

#Librerias reportes pdf
from io  import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import red
from reportlab.lib.utils import ImageReader
import PIL.Image


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
        
        baseDir = str(settings.BASE_DIR)
        
        estaEnInicio = True
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']

       
        #So no es la primera vez que inicia sesión
        nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes
        limpiezas = CalendarioMantenimiento.objects.count()
        equipos = Equipos.objects.count()
        impresoras = Impresoras.objects.count()
        empleados = Empleados.objects.count()
        
        cantidades = []
        cantidades.append([limpiezas, equipos, impresoras, empleados])
        
        limpiezas = CalendarioMantenimiento.objects.all()
        
        fecha = datetime.now()
        date = fecha.date()
        año = date.strftime("%Y") #2021
        mes = date.strftime("%m") #09
        dia = date.strftime("%d") #23
        int_dia = int(dia)
        
        mes_numero = int(fecha.month)
        
        
        arreglo_meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
        
        posicion = 0
        for mes2 in arreglo_meses:
            posicion += 1
            if posicion == mes_numero:
                mes_texto = mes2
        
        
        
        datosLimpiezas = []
        for limpieza in limpiezas:
            fecha = limpieza.fecha  #23 08 2021
            año_limpieza = fecha.strftime("%Y") #2021
            mes_limpieza = fecha.strftime("%m") #08
            dia_limpieza = fecha.strftime("%d") #23
            int_dia_limpieza = int(dia_limpieza)
            
            resta = int(mes) - int(mes_limpieza)
            
            resta_dias= int(dia)+4 #27
            
            if año_limpieza == año:
                
                if resta == 1:
                    if int_dia_limpieza >= int_dia and int_dia_limpieza <= resta_dias:
                        
                        #si está dentro del mes y 4 días más
                        
                        if limpieza.operacion == "Limpieza externa - Limpieza interna - ":
                            id_equipo = limpieza.id_equipo_id
                            
                            intEquipo = int(id_equipo)
                            datosEquipo = Equipos.objects.filter(id_equipo = intEquipo)
                            
                            for datoEquipo in datosEquipo:
                                id_empleado = datoEquipo.id_empleado_id
                                id_equipo = datoEquipo.id_equipo
                                tipo = datoEquipo.tipo
                                marca = datoEquipo.marca
                                modelo = datoEquipo.modelo
                                
                                if id_empleado == None:
                                    fecha = limpieza.fecha   
                                    datosLimpiezas.append(["Sin","Propietario",tipo,marca,modelo, fecha])
                                
                                else:
                                    
                                    datosEmpleado = Empleados.objects.filter(id_empleado = id_empleado)
                                        
                                    for datoEmpleado in datosEmpleado:
                                        nombree = datoEmpleado.nombre
                                        apellidose = datoEmpleado.apellidos
                                        
                                    fecha = limpieza.fecha   
                                    datosLimpiezas.append([nombree,apellidose,tipo,marca,modelo, fecha])
                
            
            
                
        cartuchos = Cartuchos.objects.all()
        
        impresoras = []
        
        for cartucho in cartuchos:
            id_impresora = cartucho.id_impresora_id
            
            info_impresora = Impresoras.objects.filter(id_impresora = id_impresora)
            
            for dato in info_impresora:
                marca = dato.marca
                modelo = dato.modelo
                nombreCompletoi = marca + " " + modelo
                
            impresoras.append(nombreCompletoi)
            
        lista = zip(cartuchos, impresoras)
        
        #Renovación de equipos
        equipos_renovacion = Renovacion_Equipos.objects.all()
        
        fecha = datetime.now()
        date = fecha.date()
        año = date.strftime("%Y") #2021
        mes = date.strftime("%m") #09
        
        equipos_año = []
        
        for equipo in equipos_renovacion:
            fecha_renovacion = equipo.fecha_renov #20 Octubre 2021    -     2021-10-22
            año_renovacion = fecha_renovacion.strftime("%Y")
            if año_renovacion == año:
                mes_renovacion = fecha_renovacion.strftime("%m") #10
                
                if mes_renovacion >= mes:
                    
                    resta = int(mes_renovacion) - int(mes)  #1
                
                    if resta >= 0 and resta <= 2:
                        id_equipo = equipo.id_equipo_id
                        fecha_compra = equipo.fecha_compra
                        fecha_renovacion2 = equipo.fecha_renov
                        
                        datos_equipo = Equipos.objects.filter(id_equipo = int(id_equipo))
                        
                        for dato in datos_equipo:
                            id = dato.id_equipo
                            tipo = dato.tipo
                            marca = dato.marca
                            modelo = dato.modelo
                            datos_equipo2 = str(id) + " - " + tipo + " " + marca + " " + modelo
                            id_empleado = dato.id_empleado_id
                            
                            datos_empleado = Empleados.objects.filter(id_empleado = id_empleado)
                            for em in datos_empleado:
                                nombre = em.nombre
                                apellidos = em.apellidos
                            nombre_empleado = nombre + " " + apellidos
                        
                        equipos_año.append([datos_equipo2, nombre_empleado, fecha_compra, fecha_renovacion2])
                        
        #Renovación de impresoras
        impresoras_renovacion = Renovacion_Impresoras.objects.all()
        
        fecha = datetime.now()
        date = fecha.date()
        año = date.strftime("%Y") #2021
        mes = date.strftime("%m") #09
        

        
        impresoras_año = []
        
        for impresora in impresoras_renovacion:
            fecha_renovacion = impresora.fecha_renov #20 Octubre 2021    -     2021-10-22
            año_renovacion = fecha_renovacion.strftime("%Y")
            if año_renovacion == año:
                mes_renovacion = fecha_renovacion.strftime("%m") #10
                
                if mes_renovacion >= mes:
                    
                    resta = int(mes_renovacion) - int(mes)  #1
                
                    if resta >= 0 and resta <= 2:
                        id_impresora = impresora.id_impresora_id
                        fecha_compra = impresora.fecha_compra
                        fecha_renovacion2 = impresora.fecha_renov
                        
                        datos_impresora = Impresoras.objects.filter(id_impresora = int(id_impresora))
                        
                        for dato in datos_impresora:
                            id = dato.id_impresora
                            marca = dato.marca
                            modelo = dato.modelo
                            datos_impresora2 = str(id) +  marca + " " + modelo
                            id_departamento = dato.id_area_id
                            
                            datos_area= Areas.objects.filter(id_area = id_departamento)
                            for imp in datos_area:
                                nombre = imp.nombre
                                color= imp.color
                            
                        
                        impresoras_año.append([datos_impresora2, nombre, color, fecha_compra, fecha_renovacion2])
                    
                    
                        
                
                
          #Si es la primera vez que inicia sesión.. Bienvenida 
        if "recienIniciado" in request.session:
            nombreCompleto = nombre + " " + apellidos #Blanca Yesenia Gaeta Talamantes

            del request.session['recienIniciado']

            recienIniciado = True
            
            return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo, "recienIniciado":recienIniciado, "nombre": nombre, "cantidades":cantidades, "datosLimpiezas":datosLimpiezas, 
                                                      "lista":lista, "baseDir":baseDir, "equipos_año":equipos_año, "impresoras_año":impresoras_año, "dia":dia, "mes_texto":mes_texto, "resta_dias":resta_dias, "año":año})
        else:
            return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio, "nombreCompleto":nombreCompleto, "correo":correo, "cantidades":cantidades, "datosLimpiezas":datosLimpiezas, 
                                                      "lista":lista, "baseDir":baseDir,"equipos_año":equipos_año, "impresoras_año":impresoras_año,  "dia":dia, "mes_texto":mes_texto, "resta_dias":resta_dias, "año":año})
    
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
    
    cantidad_empleados = []
    
    for area in infoAreas:
        id_area_una = area.id_area
        areaInt = int(id_area_una)
        
        empleadosEnArea = Empleados.objects.filter(id_area_id__id_area__icontains = areaInt)
        
        numero_empleados = 0
        for empleado in empleadosEnArea:
            numero_empleados+=1
        
        cantidad_empleados.append(numero_empleados)
        
    listaAreas = zip(infoAreas, cantidad_empleados)

    return render(request, "Areas/verAreas.html", {"estaEnVerAreas":estaEnVerAreas, "nombreCompleto":nombreCompleto, "correo":correo, "listaAreas":listaAreas})

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
            mensajeError = "El departamento " + area + " ya existe en la base de datos"
            return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "arregloColores":colores, "nombresColores":nombresColores,
            "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, "error": errorExiste,
            "mensaje": mensajeError})
        else:
            
            registro = Areas(nombre=area, color=color)
            registro.save()
            guardadoExito = True
            mensajeExito = "El departamento " + area + " fue agregado exitosamente"
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
        
    for id in areasEnActivos:
        datosArea = Areas.objects.filter(id_area__icontains = id) 
        
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
    
    #Notificaciones altas y bajas
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
    id_empleado_admin = request.session['idSesion']
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    #información de areas para select
    info_areas = Areas.objects.only('id_area', 'nombre', 'color')

    if request.method == "POST":

        nombre_recibido = request.POST['nombreEm']
        apellido_recibido = request.POST['apellidoEm']
        area_recibida = request.POST['areaEm']
        puesto_recibido = request.POST['puestoEm']
        correo_recibido = request.POST['correoEm']
        contra_recibida = request.POST['contraEm']
        imagen_recibida = request.FILES.get('imgempleado')

 
        lista_empleados = Empleados.objects.all()

        for empleado in lista_empleados:
            if empleado.apellidos == apellido_recibido and empleado.correo == correo_recibido:
                yaExiste = True
                texto_error = "El empleado "+ empleado.nombre + " ya existe en la Base de Datos!"
                return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "yaExiste":yaExiste, "textoError":texto_error})
            else:
                noExiste = True
                if imagen_recibida == "":
                    registro = Empleados(nombre=nombre_recibido, apellidos=apellido_recibido, 
                    id_area = Areas.objects.get(id_area = area_recibida), puesto=puesto_recibido, correo = correo_recibido, contraseña=contra_recibida, activo = "A" )
                    registro.save()
                    
                    datosEmpleado = Empleados.objects.filter(apellidos = apellido_recibido)
                    
                    for dato in datosEmpleado:
                        id_empleado_agregado = dato.id_emplado
                    
                    nombreCompletoEmp = nombre_recibido + " " + apellido_recibido
                    texto = "Se agregó al empleado "+ nombreCompletoEmp
                    fecha = datetime.now()
                    registro_bitacora = Bitacora(id_empleado = Empleados.objects.get(id_empleado = id_empleado_admin), tabla = "Empleados", id_objeto = id_empleado_agregado, operacion = texto, fecha_hora = fecha)
                    registro_bitacora.save()
                    
                    texto_existe = "El empleado "+ nombre_recibido + " fue agregado exitosamente!"
                    return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "noExiste":noExiste, "textoExiste":texto_existe})
                else:
                    registro = Empleados(nombre=nombre_recibido, apellidos=apellido_recibido, 
                    id_area = Areas.objects.get(id_area = area_recibida), puesto=puesto_recibido, correo = correo_recibido, contraseña=contra_recibida,imagen_empleado = imagen_recibida, activo = "A" )
                    registro.save()
                    
                    datosEmpleado = Empleados.objects.filter(apellidos = apellido_recibido)
                    
                    for dato in datosEmpleado:
                        id_empleado_agregado = dato.id_empleado
                    
                    nombreCompletoEmp = nombre_recibido + " " + apellido_recibido
                    texto = "Se agregó al empleado "+ nombreCompletoEmp
                    fecha = datetime.now()
                    registro_bitacora = Bitacora(id_empleado = Empleados.objects.get(id_empleado = id_empleado_admin), tabla = "Empleados", id_objeto = id_empleado_agregado, operacion = texto, fecha_hora = fecha)
                    registro_bitacora.save()
                    
                    texto_existe = "El empleado "+ nombre_recibido + " fue agregado exitosamente!"
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
        if id == None:
            datosAreasEnActivos.append(["", "", "", ""])
            
        elif id != None:
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
    
    
    
    if "idEquipoBaja" in request.session:
        bajaEquipo=True
        bajaExito= "Se dió de baja el " + request.session["idEquipoBaja"] + " con éxito!"
        del request.session["idEquipoBaja"]
        return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "bajaEquipo":
            bajaEquipo, "bajaExito": bajaExito, "equiposInactivos":equiposInactivos})
        
    if "idEquipoAlta" in request.session:
        altaEquipo= True
        altaExito= "Se dió de alta el " + request.session["idEquipoAlta"] + " con éxito"
        del request.session["idEquipoAlta"]
        return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,
                                                           "altaEquipo": altaEquipo, "altaExito":altaExito})

    return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "equiposInactivos":equiposInactivos})

def infoEquipo(request):
    estaEnVerEquipos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        
        idEquipo_recibido = request.POST['idEquipo']
        
        datosEquipo = Equipos.objects.filter(id_equipo=idEquipo_recibido)
        for datos in datosEquipo:
            id_equipo= datos.id_equipo
            propietario= datos.id_empleado
            
            sinPropietario = False
            if propietario == None:
                sinPropietario = True
                
                datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
                for datos in datosRenovacion:
                    compra= datos.fecha_compra
                    renovar=  datos.fecha_renov
                
                #sinPropietario es true
                
                mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo__icontains=id_equipo)
                if mantenimientos:
                    return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                       "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario, "mantenimientos":mantenimientos})
                else:
                      return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                       "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario})  
            
            else:
                datosPropietario= Empleados.objects.filter(id_empleado=propietario)
                for datos in datosPropietario:
                    nombre= datos.nombre
                    apellidos=datos.apellidos
                    nombreEmpleado= nombre + " " + apellidos
                    departamento=datos.id_area
                    datosDepa= Areas.objects.filter(id_area=departamento)
                    for datos in datosDepa:
                        nombreArea= datos.nombre
                        colorArea=datos.color
                        
                        
                datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
                for datos in datosRenovacion:
                    compra= datos.fecha_compra
                    renovar=  datos.fecha_renov
                    
        
                #sinPropietario es falso
                mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo__icontains=id_equipo)
                
                if mantenimientos:
                    return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                       "nombreEmpleado": nombreEmpleado, "nombreArea": nombreArea, "colorArea": colorArea, "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario,
                                                       "mantenimientos":mantenimientos})
                else:
                    return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                       "nombreEmpleado": nombreEmpleado, "nombreArea": nombreArea, "colorArea": colorArea, "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario})

    

def agregarEquipos(request):

    estaEnAgregarEquipos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    info_empleados = Empleados.objects.only('id_empleado', 'nombre', 'apellidos') #todos los empleados
    empleadosEquipo = Equipos.objects.only('id_empleado_id') #Los ids de los empleados que estan con equipos
    empleadosiEq= []
    empleadosnoEq= []
    
    
                

    
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
        cargador_recibido = request.POST['cargador']
        fecha_compra_recibido = request.POST['fecha_compra'] #dia/mes/año 29/06/2018

        if request.POST.get('activoEm', True):
            activo_recibido = "A"
        elif request.POST.get('activoEm', False):
            activo_recibido = "I"
            
        fecha_separada = fecha_compra_recibido.split("/") #29   06    2018            2018     29   06
        fecha_normal = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
        
        año_compra = int(fecha_separada[2])
        año_renov = año_compra + 3
        
        
        
        
        fecha_renovacion =  str(año_renov) + "-" + fecha_separada[0] + "-" + fecha_separada[1]
        
        
            
        if propietario_recibida == "nopropietario":
            if cargador_recibido == "":
                
                registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                estado=estado_recibida, activo="I")
                if registroCompu:
                    registroCompu.save()
                    
                    registros = Equipos.objects.count()
                    
                    registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = registros), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                    registroAntiguiedad.save()
            else:
                registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                estado=estado_recibida, activo="I", modelocargador = cargador_recibido)
                if registroCompu:
                    registroCompu.save()
                    
                    ultimo_registro = Equipos.objects.all().last()
                    
                    for dato in ultimo_registro:
                        id_equipo_agregado = dato.id_equipo
                    
                    registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = id_equipo_agregado), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                    registroAntiguiedad.save()
            compuSin = True
            textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " sin propietario!"
            return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "compuSin": compuSin, "textoCompu":textoCompu})
            
            
        elif propietario_recibida != "nopropietario":
            infoEmpleado = Empleados.objects.filter(id_empleado__icontains=propietario_recibida)
            
            for dato in infoEmpleado:
                nombre = dato.nombre
                
            compuCon= True
            textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " asignada al empleado " + nombre +"!"
            
            if cargador_recibido == "":
                
                registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                id_empleado =Empleados.objects.get(id_empleado = propietario_recibida),estado=estado_recibida, activo="A")
                if registroCompu:
                    registroCompu.save()
                    
                    ultimo_registro = Equipos.objects.all().last()
                    
                    for dato in ultimo_registro:
                        id_equipo_agregado = dato.id_equipo
                    
                    registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = id_equipo_agregado), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                    registroAntiguiedad.save()
            else: 
                registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                id_empleado =Empleados.objects.get(id_empleado = propietario_recibida),estado=estado_recibida, activo="A", modelocargador = cargador_recibido)
                if registroCompu:
                    registroCompu.save()
                    
                    ultimo_registro = Equipos.objects.all().last()
                    
                    for dato in ultimo_registro:
                        id_equipo_agregado = dato.id_equipo
                    
                    registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = id_equipo_agregado), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                    registroAntiguiedad.save()
            return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "compuCon": compuCon, "textoCompu":textoCompu})
    
    if empleadosEquipo:
        
        for empleados in info_empleados:
            for emplEq in empleadosEquipo:
                if empleados.id_empleado == emplEq.id_empleado_id:
                    empleadosiEq.append(empleados.id_empleado)
                else:
                    empleadosnoEq.append([empleados.id_empleado,empleados.nombre,empleados.apellidos])
                    
        return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo,"info_empleados":info_empleados })
    
    return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "nombreCompleto":nombreCompleto, "correo":correo,"info_empleados": info_empleados})

def renovacionEquipos(request):
    
    estaEnRenovacionEquipos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    equiposRenov = Renovacion_Equipos.objects.all()
    datosTabla = []
    for dato in equiposRenov:
        idEquipo= dato.id_equipo_id
        fechaCompra= dato.fecha_compra
        fechaRenov= dato.fecha_renov
        datosEquipo=Equipos.objects.filter(id_equipo=idEquipo)
        for datos in datosEquipo:
            tipo= datos.tipo
            marca= datos.marca
            modelo= datos.modelo
            color=datos.color
            propietario= datos.id_empleado_id
            
            equipoDatos= tipo + " " + marca + " " + modelo + " " + color
            if propietario == None:
                empleadoDatos= "Sin propietario"
                departamento= "Sin departamento"
            else:
                int_propietario = int(propietario)
                datosEmpleado= Empleados.objects.filter(id_empleado__icontains=int_propietario)
                for datosEmpl in datosEmpleado:
                    nombre= datosEmpl.nombre
                    apellidos=datosEmpl.apellidos
                    area=datosEmpl.id_area_id
                    int_area = int(area)
                    datos_areas = Areas.objects.filter(id_area = int_area)
                    for dato in datos_areas:
                        departamento = dato.nombre
                    empleadoDatos = nombre + " " + apellidos
                
        datosTabla.append([idEquipo, equipoDatos, empleadoDatos, departamento, fechaCompra, fechaRenov])
                
        
       
    
    return render(request, "Equipos/renovacionEquipos.html", {"estaEnRenovacionEquipos": estaEnRenovacionEquipos, "nombreCompleto":nombreCompleto, "correo":correo, "datosTabla":datosTabla})

def verImpresoras(request):

    estaEnVerImpresoras = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    
    impresorasActivas = Impresoras.objects.filter(activo__icontains= "A")
    impresorasInactivas = Impresoras.objects.filter(activo__icontains= "I")
    
    #impresoras Actvos
    areasEnActivos = []
    datosAreasEnActivos = []
    
    for impresoras in impresorasActivas:
        areasEnActivos.append(impresoras.id_area_id)
        #areasEnActivos = ["1"]
        
    for id in areasEnActivos:
        datosArea = Areas.objects.filter(id_area__icontains = id) #["1", "Sistemas", "rojo"]
        
        if datosArea:
            for dato in datosArea:
                nombreArea = dato.nombre
                colorArea = dato.color
        
        datosAreasEnActivos.append([nombreArea, colorArea])
        
    lista = zip(impresorasActivas, datosAreasEnActivos)
    
    #impresoras inactivos
    areasEnInactivos = []
    datosAreasEnInactivos = []
    
    for impresoras in impresorasInactivas:
        areasEnInactivos.append(impresoras.id_area_id)
        #areasEnActivos = ["1"]
        
    for id in areasEnInactivos:
        datosArea = Areas.objects.filter(id_area__icontains = id) #["1", "Sistemas", "rojo"]
        
        if datosArea:
            for dato in datosArea:
                nombreArea = dato.nombre
                colorArea = dato.color
        
        datosAreasEnInactivos.append([nombreArea, colorArea])
        
    lista2 = zip(impresorasInactivas, datosAreasEnInactivos)
    
    if "idImpresoraAlta" in request.session:
        alta = True
        mensaje = "Se dio de alta la impresora " + request.session['idImpresoraAlta']
        del request.session["idImpresoraAlta"]
        return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                           "lista2":lista2, "alta": alta, "mensaje": mensaje})
    if "idImpresoraBaja" in request.session:
        baja = True
        mensaje = "Se dio de baja la impresora " + request.session['idImpresoraBaja']
        del request.session["idImpresoraBaja"]
        return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                           "lista2":lista2, "baja": baja, "mensaje": mensaje})

    return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                           "lista2":lista2})

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
        ip_recibida = request.POST['ip']
        fecha_compra_recibido = request.POST['fecha_compra'] #dia/mes/año 29/06/2018
        red_recibido = "S"
        
        if ip_recibida == "":
            ip_recibida = "No ip"
            red_recibido = "N"    
        
        fecha_separada = fecha_compra_recibido.split("/") #29   06    2018            2018     29   06
        fecha_normal = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
        
        año_compra = int(fecha_separada[2])
        año_renov = año_compra + 3
        
        fecha_renovacion =  str(año_renov) + "-" + fecha_separada[0] + "-" + fecha_separada[1]
    
        registroImpresora=Impresoras(marca=marca_recibido, modelo= modelo_recibido,numserie=numserie_recibida,
                                     imagen=imagen_recibida, tipo=tipo_recibida,enred=red_recibido, 
                                     ip=ip_recibida, estado=estados_recibida, activo= "A",id_area = Areas.objects.get(id_area = areas_recibida))
        if registroImpresora:
                    registroImpresora.save()
                    
                    registros = Impresoras.objects.count()
                    
                    registroAntiguiedad = Renovacion_Impresoras(id_impresora = Impresoras.objects.get(id_impresora = registros), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                    registroAntiguiedad.save()
        
        impresoraAgregada = True
        
        impresoraExito= "La impresora " + marca_recibido + " " + modelo_recibido + " se guardó con éxito" 
        return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas,
                                                                    "impresoraAgregada":impresoraAgregada, "impresoraExito": impresoraExito})
         
    
            
    
            
        
    
    
    
    return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas})

def renovacionImpresoras(request):
    estaEnRenovacionImpresoras = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    ImpresorasRenov = Renovacion_Impresoras.objects.all()
    datosTabla = []
    for dato in ImpresorasRenov:
        idImpresora= dato.id_impresora_id
        fechaCompra= dato.fecha_compra
        fechaRenov= dato.fecha_renov
        datosImpresora=Impresoras.objects.filter(id_impresora=idImpresora)
        for datos in datosImpresora:
            marca= datos.marca
            modelo= datos.modelo
            imagen=datos.imagen
            departamento= datos.id_area_id
            
            impresoraDatos= marca + " " + modelo
       
            int_area = int(departamento)
            datosArea= Areas.objects.filter(id_area__icontains=int_area)
            for datos in datosArea:
                nombre= datos.nombre
                color= datos.color
                
        datosTabla.append([idImpresora, impresoraDatos, imagen, nombre, color, fechaCompra, fechaRenov])
    
    
    
    return render(request, "Impresoras/renovacionImpresoras.html", {"estaEnRenovacionImpresoras":estaEnRenovacionImpresoras, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                    "datosTabla":datosTabla})

def verInsumos(request):

    Insumos = True
    estaEnVerInsumos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    datosCartuchos = Cartuchos.objects.all()
    
    impresoras = []
    for cartuchos in datosCartuchos:
        idImpresora = cartuchos.id_impresora
        
        datosimpresoras = Impresoras.objects.filter(id_impresora__icontains=idImpresora)
         
      
        if datosimpresoras:
         for  datos in datosimpresoras:
             marcaImpresora = datos.marca
             modeloImpresora = datos.modelo
            
        impresoras.append([marcaImpresora, modeloImpresora])
    
    if "idInsumoActualizado" in request.session:
        insumoActualizado=True
        textoActualizado= request.session['idInsumoActualizado']
        del request.session["idInsumoActualizado"]
        
        return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos, "nombreCompleto":nombreCompleto, "correo":correo, "impresoras": impresoras, 
                                                      "datosCartuchos":datosCartuchos, "insumoActualizado":insumoActualizado, "textoActualizado":textoActualizado})    
    
    return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos, "nombreCompleto":nombreCompleto, "correo":correo, "impresoras": impresoras, 
                                                      "datosCartuchos":datosCartuchos})

def agregarInsumos(request):

    estaEnAgregarInsumos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    Insumos = True
    datosImpresoras = Impresoras.objects.all()
    if request.method == "POST":
        
        marca_recibido = request.POST['marcas']
        modelo_recibido = request.POST['modelo']
        cantidad_recibida = request.POST['cantidad']
        numserie_recibida = request.POST['serie']
        color_recibida = request.POST['colores']
        imagen_recibida = request.FILES.get('imagenCartucho')
        impresora_recibida = request.POST['impresora']
       
        
  
    
        registroInsumos=Cartuchos(marca=marca_recibido, modelo= modelo_recibido,nuserie=numserie_recibida, cantidad= cantidad_recibida, color= color_recibida,
                                     imagenCartucho=imagen_recibida,id_impresora = Impresoras.objects.get(id_impresora= impresora_recibida))
        registroInsumos.save()
        insumoAgregado = True
        
        insumoExito= "El insumo " + marca_recibido + " " + modelo_recibido + " se guardó con éxito" 
        return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                         "datosImpresoras":datosImpresoras, "insumoAgregado": insumoAgregado, "insumoExito": insumoExito})
    
    return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                         "datosImpresoras":datosImpresoras})

def actualizarInsumos(request):
    
    Insumos = True
    estaEnVerInsumos = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        
        id_cartucho_recibido = request.POST['idCartucho']
        cantida_recibida = request.POST['cantidadCartucho']
        
        datosCartucho = Cartuchos.objects.filter(id_cartucho__icontains=id_cartucho_recibido)
        
        for dato in datosCartucho:
            marca = dato.marca
            modelo = dato.modelo
            idimpresora = dato.id_impresora_id
            
        datosImpresora = Impresoras.objects.filter(id_impresora__icontains = idimpresora)
        
        for dato in datosImpresora:
            marcaImpresora = dato.marca
            modeloImpresora = dato.modelo
        
        actualizar = Cartuchos.objects.filter(id_cartucho__icontains=id_cartucho_recibido).update(cantidad=cantida_recibida)
        
        textoCartucho = "Se ha actualizado el stock del cartucho "+marca+" "+modelo+" de la impresora "+marcaImpresora + " "+modeloImpresora +"!"
            
        request.session['idInsumoActualizado'] = textoCartucho
        
        return redirect('/verInsumos/')
    
    

def verProgramas(request):

    estaEnVerProgramas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    registrosProgramas = Programas.objects.all()
    
    if request.method == "POST":
        
        id_area_recibido = request.POST['idArea']
        
        datosArea = Areas.objects.filter(id_area__icontains=id_area_recibido)
        
        for dato in datosArea:
            nombreArea = dato.nombre
            colorArea = dato.color
            
        programas= Programas.objects.all()
        programasArea = ProgramasArea.objects.all()
        
        programasCasillas = []
        
        for programa in registrosProgramas:
            idPrograma = int(programa.id_programa)
            programaEncontrado = ProgramasArea.objects.filter(id_programa_id__id_programa__icontains=idPrograma) #(1,1), (1,6), (1,7)
            areasPrograma=[]
            n=0
            
            if programaEncontrado:
                n=1111
            else: #El arreglo no arroja nada
                n=12414123423423423
            for programassi in programaEncontrado:
                areasPrograma.append(programassi.id_area_id)
                
                
            if int(id_area_recibido) in areasPrograma:
                programasCasillas.append([programa.id_programa, "1"])
            else:
                programasCasillas.append([programa.id_programa, "0"])
                
            
                
        lista = zip(registrosProgramas,programasCasillas)
                
                    
                    
                
        
        return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas, "nombreCompleto":nombreCompleto, "correo":correo,
                                                              "registrosProgramas": registrosProgramas, "nombreArea": nombreArea, "colorArea":colorArea, "id_area_recibido":id_area_recibido, "lista": lista,
                                                              "n":n, "programaEncontrado":programaEncontrado, "areasPrograma":areasPrograma})
    

    return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas, "nombreCompleto":nombreCompleto, "correo":correo, "registrosProgramas": registrosProgramas})



def agregarProgramas(request):

    estaEnAgregarProgramas = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        
        nombreVersion_recibido = request.POST['nombre']
        tipo_recibido = request.POST['tipo']
        licencia_recibido = request.POST['licencia']
        idioma_recibido = request.POST['idioma']
        so_recibido = request.POST['sistemaOp']
        ram_recibido = request.POST['ram']
        procesador_recibido = request.POST['procesador']
        logo_recibido = request.FILES.get('logo')
        
        registroPrograma = Programas(nombre_version=nombreVersion_recibido, tipo= tipo_recibido, licencia=licencia_recibido, idioma=idioma_recibido, sistemaoperativo_arq= so_recibido,
                                     memoria_ram=ram_recibido, procesador=procesador_recibido, imagenPrograma=logo_recibido)
        
        registroPrograma.save()
        
        registroExito =True
        mensajeExito = "Se a guardado el " + nombreVersion_recibido + " con éxito"
        return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas, "nombreCompleto":nombreCompleto, "correo":correo, "registroExito": registroExito,
                                                                 "mensajeExito":mensajeExito})
        
        
    
    

    return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas, "nombreCompleto":nombreCompleto, "correo":correo})

def actualizarProgramasArea(request):
    estaEnverProgramasPorArea = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        
        id_area_actualizar = request.POST['idArea']
        
        lista_programas = Programas.objects.all() #3
        
        for programa in lista_programas:
            id_programa = programa.id_programa #1, 2, 3
            
            nameInput = "area"+str(id_area_actualizar)+"programa"+str(programa.id_programa)
            
            if request.POST.get(nameInput, False): #Checkeado
                areaTienePrograma = True
            elif request.POST.get(nameInput, True): #No checkeado
                areaTienePrograma = False
                
            if areaTienePrograma:
                idPrograma = int(programa.id_programa)
                programaGuardado = ProgramasArea.objects.filter(id_programa_id__id_programa__icontains=idPrograma) #(1,1), (1,6), (1,7)
                
                areasPrograma=[]
                
                for area in programaGuardado:
                    areasPrograma.append(area.id_area_id)
                    
                    
                if int(id_area_actualizar) in areasPrograma:
                    #No guardar nada..
                    nada = True
                else: #No esta esa área en la tabla, agregarlo
                    registro = ProgramasArea(id_area = Areas.objects.get(id_area= id_area_actualizar), id_programa = Programas.objects.get(id_programa = idPrograma))
                    registro.save()
            
            elif areaTienePrograma == False: #No checkeado, verificar si está chequeado
                idPrograma = int(programa.id_programa)
                programaGuardado = ProgramasArea.objects.filter(id_programa_id__id_programa__icontains=idPrograma) #(1,1), (1,6), (1,7)
                
                areasPrograma=[]
                
                for area in programaGuardado:
                    areasPrograma.append(area.id_area_id)
                    
                    
                if int(id_area_actualizar) in areasPrograma:
                    area = int(id_area_actualizar)
                    borrado = ProgramasArea.objects.get(id_area_id__id_area__icontains = area, id_programa_id__id_programa__icontains = idPrograma)
                    borrado.delete()
                    
                else: #No esta esa área en la tabla, agregarlo
                    #no va aguardar nada
                    nada = True
         
        return redirect("/ProgramaPorArea/")   
            
    
    
    return redirect("/ProgramaPorArea/")
    
    
    



def ProgramasporArea(request):

    estaEnverProgramasPorArea = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    areas = Areas.objects.all()
    
    cantidadProgramas=[]
    
    for area in areas:
        numeroDeProgramas = ProgramasArea.objects.filter(id_area_id = area.id_area).count #1
        if numeroDeProgramas:
            cantidadProgramas.append(numeroDeProgramas)
        else:
            cantidadProgramas.append("0")
            
    lista = zip(areas,cantidadProgramas)
        
    
                
        

    return render(request,"Programas/verProgramasArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista})

def verProgramasPorArea(request):
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos

    if request.method == "POST":
        
        nombreArea = request.POST['nombreArea']
        datosArea = Areas.objects.filter(nombre__icontains = nombreArea)
        
        for dato in datosArea:
            idArea = dato.id_area
            
        datosAreasProgramas = ProgramasArea.objects.filter(id_area_id = idArea)
        
        arregloProgramas =[]
        
        for datos in datosAreasProgramas:
            arregloProgramas.append(datos.id_programa_id)
            
        arregloDatosProgramas = []
        
        for dato in arregloProgramas:
            datosPrograma = Programas.objects.filter(id_programa = dato)
            
            for programa in datosPrograma:
                id = programa.id_programa
                nombre = programa.nombre_version
                tipo = programa.tipo
                licencia = programa.licencia
                idioma = programa.idioma
                sistemaoperativo = programa.sistemaoperativo_arq
                memoria = programa.memoria_ram
                procesador = programa.procesador
                imagen = programa.imagenPrograma
                
            arregloDatosProgramas.append([id,nombre,tipo,licencia,idioma,sistemaoperativo,memoria,procesador,imagen])
        
        #nombreArea = Administracion

        estaEnverProgramasPorArea = True
        return render(request, "Programas/tablaProgArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "nombreArea":nombreArea, "nombreCompleto":nombreCompleto, "correo":correo, "idArea":idArea, "arregloDatosProgramas":arregloDatosProgramas})

    

def calendarioMant(request):

    estaEnCalendario = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    registroEquipos = CalendarioMantenimiento.objects.all()
    #propietarioCompu = Empleados.objects.all()
    #equipos= Equipos.objects.all()
    
    equipoPropietario = []
    fechasNuevas=[]
    for equipos in registroEquipos:
        idEquipo =int (equipos.id_equipo_id)
        fecha= equipos.fecha
        operacion = equipos.operacion
        operaciones_sueltas = operacion.split(" - ") #
        
        
        if "Limpieza externa" in operaciones_sueltas or "Limpieza interna" in operaciones_sueltas:
            nueva_fecha = fecha + relativedelta(months=1)
            fechasNuevas.append(nueva_fecha)
        else:
            fechasNuevas.append("")
                
        
        
        equi = Equipos.objects.filter(id_equipo=idEquipo)
            
        for datosEquipo in equi:
            marca = datosEquipo.marca
            modelo = datosEquipo.modelo
            idPropietario = datosEquipo.id_empleado_id
                
            if idPropietario == None:
                equipoPropietario.append(["Sin"," Propietario", marca,modelo])
            else:
                
                datosEmpleado = Empleados.objects.filter(id_empleado = idPropietario)
                
                for propietario in datosEmpleado:
                    idPropietario= int(propietario.id_empleado)
                    prop = Empleados.objects.filter(id_empleado= idPropietario)
                        
                    for datosProp in prop:
                        nombre= datosProp.nombre
                        apellidos = datosProp.apellidos
                        
                equipoPropietario.append([nombre,apellidos, marca,modelo])
            
    lista = zip (registroEquipos, equipoPropietario, fechasNuevas)
    
    
    
            
            
    
 

       
    
    return render(request,"Mantenimiento/calendarioMant.html", {"estaEnCalendario": estaEnCalendario, "nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "registroEquipos":registroEquipos})

def formularioMant(request):
    estaEnFormulario = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    infoEquipos = Equipos.objects.all()
    
    
    empleadosEquipo= []
    for empleado in infoEquipos:
        idEmpleado = empleado.id_empleado_id
        
        if idEmpleado == None:
            texto = "Sin propietario"
            empleadosEquipo.append([texto])

        else:
            empleados = Empleados.objects.filter(id_empleado__icontains = idEmpleado)

            for empleadoEquipo in empleados:
                nombre = empleadoEquipo.nombre
                apellidos = empleadoEquipo.apellidos
                empleadosEquipo.append([nombre,apellidos])
          
    lista = zip(infoEquipos, empleadosEquipo)
  
    if request.method == "POST":
        
        equipo_recibido = request.POST['equipoProp']
        operacion_recibido = request.POST.getlist('operacion')
        descripcion_recibida = request.POST['descripcion']
        fecha=datetime.now()
        operacionCompleta= ""
        for operacion in operacion_recibido:
            operacionCompleta+= operacion+" - "
            if operacion == "Limpieza externa" or operacion == "Limpieza interna":
                
                limpiezaEquipoExiste = CalendarioMantenimiento.objects.filter(id_equipo = equipo_recibido)
                
                if limpiezaEquipoExiste:
                    operacionEquipoExistente = CalendarioMantenimiento.objects.filter(id_equipo = equipo_recibido)
                    
                    for dato in operacionEquipoExistente:
                        operacion = dato.operacion
                    
                    operaciones = operacion.split(" - ")
                    
                    for operacion in operaciones:
                        if operacion == "Limpieza externa" or operacion == "Limpieza interna":
                            actualizacion = CalendarioMantenimiento.objects.filter(id_equipo =  equipo_recibido, operacion = "Limpieza externa - Limpieza Interna - ").update(fecha=fecha, observaciones=descripcion_recibida)
                            equipos = Equipos.objects.filter(id_equipo__icontains = equipo_recibido)
        
                            for equipo in equipos:
                                marca = equipo.marca
                                modelo = equipo.modelo
                        
                            mantExito = True
                            mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "con propietario " + nombre + " " + apellidos
                        
                            return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                                "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant  })
            
        registro = CalendarioMantenimiento(id_equipo=Equipos.objects.get(id_equipo=equipo_recibido), operacion=operacionCompleta, fecha=fecha, observaciones=descripcion_recibida)
        registro.save()
        
        equipos = Equipos.objects.filter(id_equipo__icontains = equipo_recibido)
        
        for equipo in equipos:
            marca = equipo.marca
            modelo = equipo.modelo
        
        mantExito = True
        mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "con propietario " + nombre + " " + apellidos
        
        return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant  })

    return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                "lista": lista})

def verCarta(request):
    estaEnVerCarta = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    datosRegistro = Carta.objects.all()
    
    empleados=[]
    equipos=[]
    
    for registros in datosRegistro:
        empleado= registros.id_empleado_id
        equipo = registros.id_equipo_id
        
        datosEmpleado = Empleados.objects.filter(id_empleado=empleado)
        for datos in datosEmpleado:
            nombres= datos.nombre
            apellido= datos.apellidos
            
        datosEquipos =Equipos.objects.filter(id_equipo=equipo)
        for datos in datosEquipos:
            marca=datos.marca
            modelo=datos.modelo
            
        empleados.append([nombres,apellido])
        equipos.append([marca, modelo])
    
    lista1=zip(datosRegistro,empleados,equipos)
    
    
    
    
    return render(request,"cartaCompromiso/verCarta.html", {"estaEnVerCarta": estaEnVerCarta, "nombreCompleto":nombreCompleto, "correo":correo, "lista1":lista1})

def agregarCarta(request):
    
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    equipos= Equipos.objects.all()
    empledos=Empleados.objects.all()
    cartas= Carta.objects.all()
    fecha= datetime.now()
    areas=[]
    
    
    compusInactivas = Equipos.objects.filter(id_empleado__isnull=True, estado="Funcional")
    
    for empleado in empledos:
        idarea= int(empleado.id_area_id)
        nombreArea= Areas.objects.filter(id_area__icontains=idarea)
        
        for area in nombreArea:
            nombreAreas= area.nombre
            areas.append([nombreAreas])
            
    lista=zip(empledos,areas)

    if request.method == "POST":
        
        compuS = request.POST['compuSeleccionada']
        empleSeleccionado = request.POST['empleadoSeleccionado']
        fechita = datetime.now()
        
        
        computadora = int(compuS)
        empleado = int(empleSeleccionado)
        preregistro = Carta(id_empleado = Empleados.objects.get(id_empleado = empleado), id_equipo = Equipos.objects.get(id_equipo = computadora), fecha = fechita)
        preregistro.save()
        
        actualizar_equipo = Equipos.objects.filter(id_equipo = compuS).update(id_empleado = Empleados.objects.get(id_empleado = empleSeleccionado),activo = "A")
        
        #crear variables de sesión.
        
        fecha= datetime.now()
        datosEquipo = Equipos.objects.filter(id_equipo__icontains = compuS)
      
        compuSeleccionada = True 
        empleadoDatos = Empleados.objects.filter(id_empleado__icontains=empleSeleccionado)
        
        for empleados in empleadoDatos:
            idArea= empleados.id_area_id
            
        datosArea = Areas.objects.filter(id_area=idArea)
        
        for area in datosArea:
            areaNombre= area.nombre
            color= area.color
            
      
        
    

        

        #Guardar datos en la tabla Carta de la base de datos

       
        estaEnAgregarCarta = True
        return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "nombreCompleto":nombreCompleto, "correo":correo, "equipos":equipos, "empleados": empledos, "lista":lista, "fecha":fecha,
                                                                "compusInactivas": compusInactivas, "compuSeleccionada":compuSeleccionada, "datosEquipo":datosEquipo, "empleadoDatos": empleadoDatos, "areaNombre": areaNombre, "color":color,
                                                                "fecha": fecha})

    estaEnAgregarCarta = True
    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "nombreCompleto":nombreCompleto, "correo":correo, "equipos":equipos, "empleados": empledos, "lista":lista, "fecha":fecha,
                                                                "compusInactivas": compusInactivas})
def imprimirCarta(request):
    
    if request.method == "POST":
        id_carta_recibida = request.POST['idCarta']
        
        datos_carta = Carta.objects.filter(id_carta = id_carta_recibida)
        
        for dato in datos_carta:
            empleado = int(dato.id_empleado_id)
            equipo = int(dato.id_equipo_id)
            fecha = dato.fecha
            imagen_firma = dato.firma
            
        info_empleado = Empleados.objects.filter(id_empleado = empleado)
        for dato_empleado in info_empleado:
            area = int(dato_empleado.id_area_id)
            
        info_area = Areas.objects.filter(id_area = area)
            
        for dato_area in info_area:
            nombre_area = dato_area.nombre
            color_area = dato_area.color
        
        info_equipo = Equipos.objects.filter(id_equipo = equipo)
            
        
        return render(request, "cartaCompromiso/imprimirCarta.html",{"info_equipo":info_equipo, "info_empleado":info_empleado, "nombre_area":nombre_area, "color_area":color_area, "fecha":fecha, "imagen_firma":imagen_firma})

def BitacorasEquipos(request):
    estaEnEquiposBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    datosBitacora = Bitacora.objects.filter(tabla = "Equipos")
    
    datosEntidad=[]
    
    for fila in datosBitacora:
        id_admin = fila.id_empleado_id
        tabla = fila.tabla
        id_entidad = fila.id_objeto
        operacion = fila.operacion
        fecha = fila.fecha_hora
        
        string = str(id_admin)
        
        datosEmpleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellidos = dato.apellidos
            
        datosEquipo = Equipos.objects.filter(id_equipo = id_entidad)
        for datoE in datosEquipo:
            tipo = datoE.tipo
            marca = datoE.marca
            modelo = datoE.modelo
        
        nombreAdmin = nombre + " " + apellidos
        compu = tipo + " " + marca + " " + modelo
        
        datosEntidad.append([nombreAdmin, id_entidad, compu, operacion, fecha])
    
    
    
    
    
    
    
    
    
    
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEquiposBitacora": estaEnEquiposBitacora, "nombreCompleto":nombreCompleto, "correo":correo, "datosEntidad": datosEntidad})

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
    
    datosBitacora = Bitacora.objects.filter(tabla = "Empleados")
    
    datosEntidad=[]
    
    for fila in datosBitacora:
        id_admin = fila.id_empleado_id
        id_entidad = fila.id_objeto
        operacion = fila.operacion
        fecha = fila.fecha_hora
        
        datosEmpleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellidos = dato.apellidos
            
        datosEmpleado = Empleados.objects.filter(id_empleado = id_entidad)
        for datoE in datosEmpleado:
            nombreEm = datoE.nombre
            apellidosEm = datoE.apellidos
        
        nombreAdmin = nombre + " " + apellidos
        nombreEmpleado = nombreEm + " " + apellidosEm
        
        datosEntidad.append([nombreAdmin, id_entidad, nombreEmpleado, operacion, fecha])
        
    return render(request, "Bitacora/Bitacoras.html",{"estaEnEmpleadosBitacora": estaEnEmpleadosBitacora, "nombreCompleto":nombreCompleto, "correo":correo, "datosEntidad":datosEntidad})

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
        
        idEquipo = request.POST['idEquipopdf']

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        nombreArchivo = idEquipo+".pdf"
        ubicacionArchivo = BASE_DIR + '/media/pdfequipos/'+ nombreArchivo

        path = open(ubicacionArchivo, 'rb')

        mime_type, _= mimetypes.guess_type(ubicacionArchivo)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
        return response

        #return render(request, "Equipos/equipo.html", {"idEquipo":BASE_DIR})

def descargarPDF2(request):
    
     if request.method == "POST":
        
        idEquipo = request.POST['idEquipopdf']

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        nombreArchivo = idEquipo+".pdf"
        ubicacionArchivo = BASE_DIR + '/media/pdfequipos/'+ nombreArchivo

        path = open(ubicacionArchivo, 'rb')

        mime_type, _= mimetypes.guess_type(ubicacionArchivo)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
        return response

def guardarImagen(request):
    estaEnAgregarCarta = True

    if request.method == "POST":
        
        idEquipo= request.POST['idEquipo']
        idEmpleado= request.POST['idEmpleado']
        fecha=datetime.now()
        
        canvasLargo = request.POST['canvasData']
        format, imgstr = canvasLargo.split(';base64,')
        ext = format.split('/')[-1]
        archivo = ContentFile(base64.b64decode(imgstr), name= idEmpleado+ '.' + ext)
        
        numeroFirmas = Carta.objects.count() #1
        
        registroFirma = Carta.objects.get(id_carta=numeroFirmas)
        registroFirma.firma = archivo
        registroFirma.save()
        
        #preregistro = Carta(id_empleado = Empleados.objects.get(id_empleado = idEmpleado), id_equipo = Equipos.objects.get(id_equipo = idEquipo), fecha = fecha, firma = archivo)
        #preregistro.save()
        
        imagenGuardada = True
        request.session['imagenGuardada'] = imagenGuardada
        #acutalizacion = Equipos.objects.filter(id_equipo = idEquipo).update(id_empleado = Empleados.objects.get(id_empleado = idEmpleado), activo = "A")
        
        
        return redirect('/firmarCarta/')

    return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta})

def editarEquipo(request):
    estaEnCartasBitacora = True
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        equipoRecibido = request.POST['idEquipo']
        equipoDatos = Equipos.objects.filter(id_equipo__icontains=equipoRecibido)

        
        for dato in equipoDatos:
            empleadoId= dato.id_empleado_id #2
            ramequipo = dato.memoriaram
            sistema = dato.sistemaoperativo
            
        if empleadoId == None:
            ram = ["1 GB", "2 GB", "4 GB", "8 GB", "12 GB", "16 GB", "32 GB"]
            for memoria in ram:
                if memoria == ramequipo:
                    ram.remove(memoria)
                    
            sistemasOperativos = ["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 10"]
            for sistemaOp in sistemasOperativos:
                if sistemaOp == sistema:
                    sistemasOperativos.remove(sistemaOp)
            
            empleadosTotales = Empleados.objects.all()
            
                
            sinPropietario = True
            lista = zip(equipoDatos,empleadosTotales)
            return render(request, "Editar/editarEquipo.html", {"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"ram": ram,"sistemasOperativos":sistemasOperativos, "equipoRecibido":equipoRecibido, "empleadosTotales":empleadosTotales, "sinPropietario":sinPropietario})
        else:
            
            empleado = Empleados.objects.filter(id_empleado__icontains=empleadoId)
            ram = ["1 GB", "2 GB", "4 GB", "8 GB", "12 GB", "16 GB", "32 GB"]
            for memoria in ram:
                    if memoria == ramequipo:
                        ram.remove(memoria)
                        
            sistemasOperativos = ["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 10"]
            for sistemaOp in sistemasOperativos:
                if sistemaOp == sistema:
                    sistemasOperativos.remove(sistemaOp)
              
            lista = zip(equipoDatos,empleado)
            
            empleados_totales = Empleados.objects.all()
            arreglo_ids = []
            
            for emp in empleados_totales:
                arreglo_ids.append(emp.id_empleado)
            
            #[1,2,3]
            
            for id in arreglo_ids:
                if id == empleadoId: #si 2 == 2
                    arreglo_ids.remove(id)
                    
            #[1,3]
            
            datos_empleados = []
            
            for id in arreglo_ids:
                datos = Empleados.objects.filter(id_empleado = id)
                for dato in datos:
                    id_empleado = dato.id_empleado
                    nombre_empleado = dato.nombre
                    apellidos_empleado = dato.apellidos
                datos_empleados.append([id_empleado, nombre_empleado, apellidos_empleado])    
                 
                    
            
        
            return render(request, "Editar/editarEquipo.html", {"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "ram": ram, "sistemasOperativos":sistemasOperativos, "empleado":empleado, "equipoRecibido":equipoRecibido, "datos_empleados":datos_empleados})
            
        





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
        
        areaInt = int(areaEditar)
        
        datosEmpleado = Empleados.objects.filter(correo__icontains = correoEditar)
        
        if datosEmpleado:
            for dato in datosEmpleado:
                idEmpleado = dato.id_empleado
        
        actualizacion = Empleados.objects.filter(correo__icontains = correoEditar).update(nombre=nombreEditar, apellidos=apellidoEditar,
                                                                                          id_area=areaInt, puesto=puestoEditar, 
                                                                                          correo=correoEditar, contraseña=contraseñaEditar, 
                                                                                          )
        
        
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
    
def editarEquipoBd(request):
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        equipoId = request.POST['idEquipo']
        ram_actualizar = request.POST['ram']
        propietario_actualizar = request.POST['propietario']
        sistema_actualizar = request.POST['sistema']
        estado_actualizar = request.POST['estado']
        cargador_actualizar = request.POST['cargador']
        
        
            
            
        
         
        if propietario_actualizar == "sinPropietario":
            actualizar = Equipos.objects.filter(id_equipo__icontains=equipoId).update(memoriaram=ram_actualizar, id_empleado_id=None,
                                               sistemaoperativo= sistema_actualizar, estado= estado_actualizar, modelocargador = cargador_actualizar, activo="I")
            
        elif propietario_actualizar !=  "sinPropietario": 
            int_empleado = int(propietario_actualizar)
            actualizar = Equipos.objects.filter(id_equipo__icontains=equipoId).update(memoriaram=ram_actualizar, id_empleado_id=Empleados.objects.get(id_empleado = int_empleado),
                                               sistemaoperativo= sistema_actualizar, estado= estado_actualizar, modelocargador = cargador_actualizar, activo="A")
            
        datos = Equipos.objects.filter(id_equipo__icontains = equipoId)
        
        for dato in datos:
            tipo = dato.tipo
            marca = dato.marca
            modelo = dato.modelo
            
        todoCompu = tipo + " " + marca + " " + modelo
        
        editado = True
        textoEdicion = "Se ha editado al equipo " + todoCompu + " con éxito!"
        
        
        
        
        
        
        
        
        
        
        equipoRecibido = equipoId
        equipoDatos = Equipos.objects.filter(id_equipo__icontains=equipoRecibido)

        
        for dato in equipoDatos:
            empleadoId= dato.id_empleado_id #2
            ramequipo = dato.memoriaram
            sistema = dato.sistemaoperativo
            
        if empleadoId == None:
            ram = ["1 GB", "2 GB", "4 GB", "8 GB", "12 GB", "16 GB", "32 GB"]
            for memoria in ram:
                if memoria == ramequipo:
                    ram.remove(memoria)
                    
            sistemasOperativos = ["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 10"]
            for sistemaOp in sistemasOperativos:
                if sistemaOp == sistema:
                    sistemasOperativos.remove(sistemaOp)
            
            empleadosTotales = Empleados.objects.all()
            
                
            sinPropietario = True
            lista = zip(equipoDatos,empleadosTotales)
            return render(request, "Editar/editarEquipo.html", {"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"ram": ram,"sistemasOperativos":sistemasOperativos, "equipoRecibido":equipoRecibido, "empleadosTotales":empleadosTotales, "sinPropietario":sinPropietario, 
                                                                "editado":editado, "textoEdicion":textoEdicion})
        else:
            
            empleado = Empleados.objects.filter(id_empleado__icontains=empleadoId)
            ram = ["1 GB", "2 GB", "4 GB", "8 GB", "12 GB", "16 GB", "32 GB"]
            for memoria in ram:
                    if memoria == ramequipo:
                        ram.remove(memoria)
                        
            sistemasOperativos = ["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 10"]
            for sistemaOp in sistemasOperativos:
                if sistemaOp == sistema:
                    sistemasOperativos.remove(sistemaOp)
              
            lista = zip(equipoDatos,empleado)
            
            empleados_totales = Empleados.objects.all()
            arreglo_ids = []
            
            for emp in empleados_totales:
                arreglo_ids.append(emp.id_empleado)
            
            #[1,2,3]
            
            for id in arreglo_ids:
                if id == empleadoId: #si 2 == 2
                    arreglo_ids.remove(id)
                    
            #[1,3]
            
            datos_empleados = []
            
            for id in arreglo_ids:
                datos = Empleados.objects.filter(id_empleado = id)
                for dato in datos:
                    id_empleado = dato.id_empleado
                    nombre_empleado = dato.nombre
                    apellidos_empleado = dato.apellidos
                datos_empleados.append([id_empleado, nombre_empleado, apellidos_empleado])    
                 
                    
            
        
            return render(request, "Editar/editarEquipo.html", {"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "ram": ram, "sistemasOperativos":sistemasOperativos, "empleado":empleado, "equipoRecibido":equipoRecibido, "datos_empleados":datos_empleados, 
                                                                "editado":editado, "textoEdicion":textoEdicion})
            
        
        
        
        
        
    
    return render(request,"Editar/editarEmpleado.html", { "nombreCompleto":nombreCompleto, "correo":correo})

def editarImpresoraBd(request):
    
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
    
    if request.method == "POST":
        impresora_id = request.POST['idImpresora']
        area_actualizar = request.POST['areaEditar']
        estado_actualizar = request.POST['estadoEditar']
        
        datosImpresora = Impresoras.objects.filter(id_impresora__icontains=impresora_id)
        
        for dato in datosImpresora:
            marcaMostrar = dato.marca
            modeloMostrar = dato.modelo
            
        if request.POST["ipEditar"]=="":
            laVaAPonerEnRed = False
        elif request.POST["ipEditar"] != "":
            ip_actualizar = request.POST["ipEditar"]
            laVaAPonerEnRed = True
            
        
         
        if laVaAPonerEnRed == False:
            if estado_actualizar == "Funcional":
                actualizar = Impresoras.objects.filter(id_impresora__icontains=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                               enred="N", ip="", activo = "A")
            else:
                actualizar = Impresoras.objects.filter(id_impresora__icontains=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                               enred="N", ip="", activo = "I")
        elif laVaAPonerEnRed == True:
            if estado_actualizar == "Funcional":
                actualizar = Impresoras.objects.filter(id_impresora__icontains=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                               enred="S", ip=ip_actualizar, activo = "A")
            else:
                actualizar = Impresoras.objects.filter(id_impresora__icontains=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                               enred="S", ip=ip_actualizar, activo = "I")
            
        datos_impresora = Impresoras.objects.filter(id_impresora__icontains = impresora_id)
        
        if datos_impresora:
            for datoEditar in datos_impresora:
            
                idAreaImpresora = datoEditar.id_area_id
                
        datosArea = Areas.objects.filter(id_area__icontains = idAreaImpresora)
        if datosArea:
            for nombreEditar in datosArea:
                
                nombreArea =  nombreEditar.nombre
        
        areas = Areas.objects.all()
        
        areasNuevas = []
        
        for dato in areas:
            if idAreaImpresora == dato.id_area:
                yaEsta = True
            else:
                areasNuevas.append([dato.id_area, dato.nombre])
        
        editado = True
        textoEditado = "Se ha editado la impresora " + marcaMostrar + " " + modeloMostrar + " con éxito!"
        
        return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datos_impresora, "nombreCompleto":nombreCompleto, "correo":correo, "nombreArea":nombreArea, "areasNuevas":areasNuevas, "editado":editado, "textoEditado":textoEditado})
            
        
        
        
    
    return render(request,"Editar/editarImpresora.html", { "nombreCompleto":nombreCompleto, "correo":correo})

def altaEmpleado(request):
    
    id_empleado_admin = request.session['idSesion']
    if request.method == "POST":
    
        idAlta= request.POST['idEmpleadoAlta']
        
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = idAlta)
        
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellido = dato.apellidos
            
        nombreCompletoEmp = nombre + " " + apellido
        
        actualizacion = Empleados.objects.filter(id_empleado__icontains = idAlta).update(activo = "A")
        if actualizacion:
            texto = "Se dió se alta al empleado "+nombreCompletoEmp
            fecha = datetime.now()
            registro_bitacora = Bitacora(id_empleado = Empleados.objects.get(id_empleado = id_empleado_admin), tabla = "Empleados", id_objeto = idAlta, operacion = texto, fecha_hora = fecha)
            registro_bitacora.save()
        
        request.session['idEmpleadoAlta'] = nombreCompletoEmp
        
        return redirect('/verEmpleados/')
    
def bajaEmpleado(request):
    
    id_empleado_admin = request.session['idSesion']
    if request.method == "POST":
    
        idBaja= request.POST['idEmpleadoBaja']
        
        datosEmpleado = Empleados.objects.filter(id_empleado__icontains = idBaja)
        
        for dato in datosEmpleado:
            nombre = dato.nombre
            apellido = dato.apellidos
        
        nombreCompletoEmp = nombre + " " + apellido
        
        actualizacion = Empleados.objects.filter(id_empleado__icontains = idBaja).update(activo = "I")
        if actualizacion:
            texto = "Se dió se baja al empleado "+nombreCompletoEmp
            fecha = datetime.now()
            registro_bitacora = Bitacora(id_empleado = Empleados.objects.get(id_empleado = id_empleado_admin), tabla = "Empleados", id_objeto = idBaja, operacion = texto, fecha_hora = fecha)
            registro_bitacora.save()
            
        request.session['idEmpleadoBaja'] = nombreCompletoEmp
        
        return redirect('/verEmpleados/')
    
def altaImpresora(request):
    
    if request.method == "POST":
    
        idAlta= request.POST['idImpresoraAlta']
        
        datosImpresora = Impresoras.objects.filter(id_impresora__icontains = idAlta)
        
        for dato in datosImpresora:
            marca = dato.marca
            modelo = dato.modelo
            
        nombreCompletoImp = marca + " " + modelo
        
        actualizacion = Impresoras.objects.filter(id_impresora__icontains = idAlta).update(activo = "A")
        
        
        request.session['idImpresoraAlta'] = nombreCompletoImp
        
        return redirect('/verImpresoras/')
    
def bajaImpresora(request):
    
    if request.method == "POST":
    
        idBaja= request.POST['idImpresoraBaja']
        
        datosImpresora = Impresoras.objects.filter(id_impresora__icontains = idBaja)
        
        for dato in datosImpresora:
            marca = dato.marca
            modelo = dato.modelo
        
        nombreCompletoImp = marca + " " + modelo
        
        actualizacion = Impresoras.objects.filter(id_impresora__icontains = idBaja).update(activo = "I")
        
        request.session['idImpresoraBaja'] = nombreCompletoImp
        
        return redirect('/verImpresoras/')
    
    
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
    correo = request.session['correoSesion']
    if request.method == "POST":
        
        idBaja= request.POST['idEquipoBaja']
        
        datosEquipo = Equipos.objects.filter(id_equipo__icontains = idBaja)
        
        for dato in datosEquipo:
            marca = dato.marca
            modelo = dato.modelo
        
        equipo = marca + " " + modelo
        
        actualizacion = Equipos.objects.filter(id_equipo__icontains = idBaja).update(activo = "I")
        
        datosEmpleado= Empleados.objects.filter(correo=correo)
        
        for datos in datosEmpleado:
            nombre = datos.nombre
            apellidos = datos.apellidos
            idEmpleado = datos.id_empleado
        
        texto = " Se dio de baja el equipo: "  + equipo  
        fecha = datetime.now()
        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=idEmpleado), tabla = "Equipos", id_objeto=idBaja, operacion=texto, fecha_hora= fecha)
        registroBitacora.save()
            
        
        
        
        
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
        datos_impresora = Impresoras.objects.filter(id_impresora__icontains = idImpresora)
        
        if datos_impresora:
            for datoEditar in datos_impresora:
            
                idAreaImpresora = datoEditar.id_area_id
                
        datosArea = Areas.objects.filter(id_area__icontains = idAreaImpresora)
        if datosArea:
            for nombreEditar in datosArea:
                
                nombreArea =  nombreEditar.nombre
        
        areas = Areas.objects.all()
        
        areasNuevas = []
        
        for dato in areas:
            if idAreaImpresora == dato.id_area:
                yaEsta = True
            else:
                areasNuevas.append([dato.id_area, dato.nombre])

        return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datos_impresora, "nombreCompleto":nombreCompleto, "correo":correo, "nombreArea":nombreArea, "areasNuevas":areasNuevas})

def firmarCarta(request):
    
    if "imagenGuardada" in request.session:
        
        numeroFirmas = Carta.objects.count() #1
        
        registroFirma = Carta.objects.get(id_carta=numeroFirmas)
        
        
        idEquipo = registroFirma.id_equipo_id
        idEmpleado = registroFirma.id_empleado_id
        imagen = registroFirma.firma
        imagen2 = True
        
        fecha=datetime.now()
            
            
        datosEquipo = Equipos.objects.filter(id_equipo = idEquipo)
        datosEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            
        for dato in datosEmpleado:
            idArea = dato.id_area_id
                
        datos_area = Areas.objects.filter(id_area = idArea)
            
        for datoArea in datos_area:
            nombre = datoArea.nombre
            color = datoArea.color
        
        

            #Hacer consulta al ultimo registro de la tabla de cartas, para ver la ultima carta preguardada.
        
        del request.session["imagenGuardada"]
        return render(request, "cartaCompromiso/firmarCarta.html", {"datosEquipo":datosEquipo, "datosEmpleado":datosEmpleado, "nombre":nombre, "color":color, "fecha":fecha, "imagen":imagen, "imagen2":imagen2}) 
    
    else: 
        
        numeroFirmas = Carta.objects.count() #1
            
        registroFirma = Carta.objects.get(id_carta=numeroFirmas)
        
        
        idEquipo = registroFirma.id_equipo_id
        idEmpleado = registroFirma.id_empleado_id
        
        fecha=datetime.now()
            
            
        datosEquipo = Equipos.objects.filter(id_equipo = idEquipo)
        datosEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            
        for dato in datosEmpleado:
            idArea = dato.id_area_id
                
        datos_area = Areas.objects.filter(id_area = idArea)
            
        for datoArea in datos_area:
            nombre = datoArea.nombre
            color = datoArea.color
        

            #Hacer consulta al ultimo registro de la tabla de cartas, para ver la ultima carta preguardada.
        

        return render(request, "cartaCompromiso/firmarCarta.html", {"datosEquipo":datosEquipo, "datosEmpleado":datosEmpleado, "nombre":nombre, "color":color, "fecha":fecha}) 


def reporteDepartamentos(request):
    
    #crear el http response con pdf
    respuesta = HttpResponse(content_type='application/pdf')
    respuesta['Content-Disposition'] = 'attachment; filename=Reporte Deparatmentos.pdf'
    #Crear objeto PDF 
    buffer =BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    #nombre de empresa
    c.setFont('Helvetica-Oblique', 22)
    c.drawString(40,750, 'Custom & Co S.A. de C.V.')
    #fecha
    hoy=datetime.now()
    fecha = str(hoy.date())
    
    c.setFont('Helvetica', 12)
    c.drawString(480,750, fecha)
    #linea guinda
    color_guinda="#B03A2E"
    c.setFillColor(color_guinda)
    c.setStrokeColor(color_guinda)
    c.line(40,747,560,745)
    #nombre departamento
    color_negro="#030305"
    c.setFillColor(color_negro)
    c.setFont('Helvetica', 16)
    c.drawString(60,730, 'Departamento de Sistemas')
    #titulo
    c.setFont('Helvetica-Bold', 22)
    c.drawString(180,690, 'Reporte de Departamentos')
    
    base_dir = str(settings.BASE_DIR)
    logo = base_dir+'/static/images/logopdf.png'   
    c.drawImage(logo, 250,620,120,90, preserveAspectRatio=True)
    
    
    #obtener datos de area
    
    datosAreas= Areas.objects.all()
    cantidad_empleados = []
    
    for area in datosAreas:
        id_area_una = area.id_area
        areaInt = int(id_area_una)
        
        empleadosEnArea = Empleados.objects.filter(id_area_id__id_area__icontains = areaInt)
        
        numero_empleados = 0
        for empleado in empleadosEnArea:
            numero_empleados+=1
        
        cantidad_empleados.append(numero_empleados)
        
    listaAreas = zip(datosAreas, cantidad_empleados)
    #header de tabla
    styles = getSampleStyleSheet()
    styleBH =styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10
    
    
    id_Departamento = Paragraph('''Id Departamento''', styleBH)
    nombre = Paragraph('''Nombre''', styleBH)
    color = Paragraph('''Color''', styleBH)
    numero_empleado = Paragraph('''Numero de empleados''', styleBH)
    filasTabla=[]
    filasTabla.append([id_Departamento, nombre, color, numero_empleado])
    #Tabla
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7
    
    high = 625
    for area, empleados in listaAreas:
        fila = [area.id_area, area.nombre, area.color, empleados]
        filasTabla.append(fila)
        high= high - 18 
        
    #escribir tabla
    width, height = letter
    tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm, 4 * cm, 4 * cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    
    contador = 0
    for fila in filasTabla:
        contador += 1
        if contador > 1:
            if fila[2] == "label bg-red":
                color = colors.red
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
                
            elif fila[2] == "label bg-pink":
                color = colors.pink
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-purple":
                color = colors.purple
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-indigo":
                color = colors.indigo
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-blue":
                color = colors.blue
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-cyan":
                color = colors.cyan
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-teal":
                color = colors.teal
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-green":
                color = colors.green
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-light-green":
                color = colors.lightgreen
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-lime":
                color = colors.lime
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-yellow":
                color = colors.yellow
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-amber":
                color = colors.orangered
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-orange":
                color = colors.orange
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-deep-orange":
                color = colors.deeppink
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-brown":
                color = colors.brown
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-grey":
                color = colors.gray
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-blue-grey":
                color = colors.blueviolet
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
            elif fila[2] == "label bg-black":
                color = colors.black
                tabla.setStyle(TableStyle([
                    ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                ]))
                
    
    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 80, high)
    
    #linea guinda
    color_guinda="#B03A2E"
    c.setFillColor(color_guinda)
    c.setStrokeColor(color_guinda)
    c.line(40,60,560,60)
    
    color_negro="#030305"
    c.setFillColor(color_negro)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
    
    
    c.showPage()
    
    
    
    #guardar pdf
    c.save()
    #obtener valores de bytesIO y esribirlos en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    respuesta.write(pdf)
    return respuesta

def reporteEmpleadosActivos(request):
    
    numero_empleados = Empleados.objects.count() #11 empleados
    
    division = numero_empleados // 9 #Resultado 1, sin residuo
    residuo = numero_empleados%9 #residuo hay 2
    
    
    
    if residuo == 0:
        #hojas iguales a division.
        hojasIguales = True
        
    if residuo != 0:
        division = division + 1
        
    #QUITAR ESTO PARA OTRA HOJA
    #crear el http response con pdf
    respuesta = HttpResponse(content_type='application/pdf')
    respuesta['Content-Disposition'] = 'attachment; filename=Reporte Deparatmentos.pdf'
    #Crear objeto PDF 
    buffer =BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    #HASTA AQUI
        
    hojaNueva = False
    
    for hoja in range(division):
        
        #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
        datosEmpleados= Empleados.objects.filter(activo__icontains="A")
        
        contadorEmpleados = 0
        
        areas = []
        urls_imagenes = []
        base_dir = str(settings.BASE_DIR)
        
        for empleado in datosEmpleados:
            
            contadorEmpleados += 1
            
            if contadorEmpleados <= 9:
                #Obtener solo empleados que quepan en la hoja
                idarea = empleado.id_area_id
                imagen = empleado.imagen_empleado
                urlimagen = base_dir + '/media/' + str(imagen)
                img = Image(urlimagen,50,50)
                
                urls_imagenes.append(img)
                
                info_area = Areas.objects.filter(id_area = idarea)
                
                for dato in info_area:
                    nombre = dato.nombre
                    areas.append(nombre)
            
            #solo 9 empleados
            hojaNueva = True
            listaEmpleados = zip(datosEmpleados, areas, urls_imagenes)
                
                

        
        #nombre de empresa
        c.setFont('Helvetica-Oblique', 22)
        c.drawString(40,750, 'Custom & Co S.A. de C.V.')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        
        c.setFont('Helvetica', 12)
        c.drawString(480,750, fecha)
        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,747,560,745)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 16)
        c.drawString(60,730, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
        c.drawString(180,690, 'Reporte Empleados Activos')
        
        base_dir = str(settings.BASE_DIR)
        logo = base_dir+'/static/images/logopdf.png'   
        c.drawImage(logo, 250,620,120,90, preserveAspectRatio=True)
        
        
        
        
        
        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 9
        
        
        id_empleado = Paragraph('''ID''', styleBH)
        nombre = Paragraph('''Nombre''', styleBH)
        apellido = Paragraph('''Apellido''', styleBH)
        imagen = Paragraph('''Imagen''', styleBH)
        departamento = Paragraph('''Dpto.''', styleBH)
        puesto = Paragraph('''Puesto''', styleBH)
        correo = Paragraph('''correo''', styleBH)
        pwd = Paragraph('''Contraseña''', styleBH)
        filasTabla=[]
        filasTabla.append([id_empleado, nombre, apellido, imagen, departamento, puesto, correo, pwd])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high=650
        for empleado in datosEmpleados:
            high = high - 36
        
        for empleado, areas, imagenes in listaEmpleados:
            campo_empleado = Paragraph(str(empleado.id_empleado), styleN)
            campo_nombre = Paragraph(empleado.nombre, styleN)
            campo_apellidos = Paragraph(empleado.apellidos, styleN)
            campo_area = Paragraph(areas, styleN)
            campo_puesto = Paragraph(empleado.puesto, styleN)
            campo_correo = Paragraph(empleado.correo, styleN)
            campo_contraseña = Paragraph(empleado.contraseña, styleN)
            
            fila = [campo_empleado, campo_nombre, campo_apellidos, imagenes, campo_area, campo_puesto, campo_correo, 
                    campo_contraseña]
            filasTabla.append(fila)
            
            high= high - 18 
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[1 * cm, 2 * cm, 3 * cm, 2.25 * cm, 2 * cm, 2 * cm, 4 * cm, 4 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        contador = 0
        for fila in filasTabla:
            contador += 1
            if contador > 1:
                if fila[2] == "label bg-red":
                    color = colors.red
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                    
                elif fila[2] == "label bg-pink":
                    color = colors.pink
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-purple":
                    color = colors.purple
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-indigo":
                    color = colors.indigo
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-blue":
                    color = colors.blue
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-cyan":
                    color = colors.cyan
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-teal":
                    color = colors.teal
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-green":
                    color = colors.green
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-light-green":
                    color = colors.lightgreen
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-lime":
                    color = colors.lime
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-yellow":
                    color = colors.yellow
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-amber":
                    color = colors.orangered
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-orange":
                    color = colors.orange
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-deep-orange":
                    color = colors.deeppink
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-brown":
                    color = colors.brown
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-grey":
                    color = colors.gray
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-blue-grey":
                    color = colors.blueviolet
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                elif fila[2] == "label bg-black":
                    color = colors.black
                    tabla.setStyle(TableStyle([
                        ('TEXTCOLOR', (2 , contador - 1), (-2, contador -1 ), color)
                    ]))
                    
        
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 20, high)
        
        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
        
        #guardar la pagina, y se crea otra en caso de ser necesario
        c.showPage()
        
        
        
        #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    #guardar pdf
    c.save()
    #obtener valores de bytesIO y esribirlos en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    respuesta.write(pdf)
    return respuesta
    