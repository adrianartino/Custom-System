#Librerías
from cmath import sin
from glob import escape
import mimetypes
import os
import base64
from io  import BytesIO
from sre_parse import expand_template

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Encuestas, Preguntas, Respuestas,Mouses, Teclados, Monitores, Telefonos, DiscosDuros, EmpleadosDiscosDuros, MemoriasUSB, PrestamosSistemas, SoportesTecnicos, ImplementacionSoluciones, Mochilas

#Librería para manejar archivos en Python
from django.core.files.base import ContentFile

#Librerías de fecha
from datetime import date, datetime
from datetime import timedelta
from calendar import calendar
from dateutil.relativedelta import relativedelta

#Archivo configuración Django
from django.conf import settings

#Correo
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Librerias reportes pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

#Libreria excel.
import xlwt

def notificacionInsumos():
    
    cartuchosBajos = Cartuchos.objects.filter(cantidad=1)
    cartuchosNoti = []
    for cartucho in cartuchosBajos:
        marca = cartucho.marca
        modelo = cartucho.modelo
        color = cartucho.color
        idImp = cartucho.id_impresora_id
        
        cartuchoCompleto = marca + " " + modelo + " " + color
        datosImpresora = Impresoras.objects.filter(id_impresora=idImp)
        for impresora in datosImpresora:
            marcas = impresora.marca
            modelos = impresora.modelo
        
        impresoraCompleta = marcas + " " + modelos
        cartuchosNoti.append([impresoraCompleta, cartuchoCompleto])
    
    return cartuchosNoti

def notificacionLimpiezas():
    limpiezas = CalendarioMantenimiento.objects.all()
    fecha = datetime.now()
    date = fecha.date()
    año = date.strftime("%Y") #2021
    mes = date.strftime("%m") #09
    dia = date.strftime("%d") #23
    int_dia = int(dia)
          
    limpiezasNoti = []
    for limpieza in limpiezas:
        fecha = limpieza.fecha  #23 08 2021
        año_limpieza = fecha.strftime("%Y") #2021
        mes_limpieza = fecha.strftime("%m") #08
        dia_limpieza = fecha.strftime("%d") #23
        int_dia_limpieza = int(dia_limpieza)
            
        resta = int(mes) - int(mes_limpieza)
            
        if año_limpieza == año:
                
            if resta == 1:
                if int_dia_limpieza == int_dia:
                        
                    #si está dentro del mes y el dia exacto de limpieza
                        
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
                            
                            equipoCompleto = tipo + " " + marca + " " + modelo
                            
                            if id_empleado == None:
                                fecha = limpieza.fecha   
                                empleado= "Sin Propietario"
                                
                            else:
                                
                                datosEmpleado = Empleados.objects.filter(id_empleado = id_empleado)
                                        
                                for datoEmpleado in datosEmpleado:
                                    nombree = datoEmpleado.nombre
                                    apellidose = datoEmpleado.apellidos
                                        
                                    fecha = limpieza.fecha   
                                    empleado =  nombree + " " + apellidose
                                    
                        limpiezasNoti.append([equipoCompleto, empleado])
    
    return limpiezasNoti

def numNoti():
    
    limpiezas = notificacionLimpiezas()
    cartuchos = notificacionInsumos()
    
    contadorlimp = 0
    contadorCart = 0
    for limpieza in limpiezas:
        contadorlimp += 1
    
    for cartucho in cartuchos:
        contadorCart += 1
        
    suma = contadorlimp + contadorCart
    
    num_notificaciones = str(suma)
    
    return num_notificaciones
                
            


# Create your views here.
def login(request):

    #Si ya existe una sesión
    if "idSesion" in request.session:
        if request.session['correoSesion'] == "adminSistemas0817":
                    
            return redirect('/inicio/') #redirecciona a url de inicio
        else:
            return redirect('/principal/') #redirecciona a la pagina normal del empleado

    #Si no hay una sesión iniciada
    else:

        #si se apretó el botón.
        if request.method == "POST":
            
            correousuario = request.POST['username']
            pwd = request.POST['pass']

            datosUsuario = Empleados.objects.filter(correo=correousuario)

            #Si encontro a un usuario con ese correo...
            if datosUsuario:

                for dato in datosUsuario:
                    id = dato.id_empleado
                    nombres = dato.nombre
                    apellidos = dato.apellidos
                    correo = dato.correo
                    contraReal = dato.contraseña
                    
                #Si la contraseña es igual...
                if correousuario == correo and pwd == contraReal :

                    request.session['idSesion'] = id
                    request.session['correoSesion'] = correo
                    request.session['nombres'] = nombres
                    request.session['apellidos'] = apellidos
                    request.session['recienIniciado'] = "primerInicio"
                    
                    if correousuario == "adminSistemas0817":
                    
                        return redirect('/inicio/') #redirecciona a url de inicio
                    else:
                        return redirect('/principal/') #redirecciona a la pagina normal del empleado
                    
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
        if "textoCorreo" in request.session:
            correoEnviado = True
            texto = request.session['textoCorreo']#tomar el valor de la variable de sesion..

            del request.session['textoCorreo']#se cierra la sesión del correo enviado.
            return render(request, "Login/login.html",{"correoEnviado":correoEnviado, "texto":texto})
        else:
             return render(request, "Login/login.html")

def salir(request):

    #Cerrar variables de sesión
   del request.session["idSesion"]
   del request.session['correoSesion']
   del request.session['nombres'] 
   del request.session['apellidos'] 

   return redirect('/login/')

def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto
            
    
    
def inicio(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        baseDir = str(settings.BASE_DIR)
        
        estaEnInicio = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']

        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        foto = fotoAdmin(request)
        
        
        #arreglo cantidades de filas por tabla
        limpiezas = CalendarioMantenimiento.objects.count()
        equipos = Equipos.objects.count()
        impresoras = Impresoras.objects.count()
        empleados = Empleados.objects.count()
        cantidades = []
        cantidades.append([limpiezas, equipos, impresoras, empleados])
        
        #próximas limpiezas
        limpiezas = CalendarioMantenimiento.objects.all()
        
        fecha = datetime.now()
        date = fecha.date()
        año = date.strftime("%Y") #2022
        mes = date.strftime("%m") #04
        dia = date.strftime("%d") #11
        int_dia = int(dia)
        resta_dias= int(dia)+4 #27
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
            año_limpieza = fecha.strftime("%Y") #2022
            mes_limpieza = fecha.strftime("%m") #03
            dia_limpieza = fecha.strftime("%d") #13
            int_dia_limpieza = int(dia_limpieza)
            
            resta = int(mes) - int(mes_limpieza)
            
           
          
            
            if año_limpieza == año:
                
                if resta == 1:
                    if int_dia_limpieza >= int_dia and int_dia_limpieza <= resta_dias:
                        
                        #si está dentro del mes y 4 días más
                        
                        if limpieza.operacion == "Limpieza externa, Limpieza interna":
                            
                            
                            if limpieza.id_equipo_id != None :
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
                                        
                               
                            else:
                                id_impresora = limpieza.id_impresora_id
                                intImpresora = int(id_impresora)
                                datosImpresora = Impresoras.objects.filter(id_impresora = intImpresora)
                                
                                for datoImpresora in datosImpresora:
                                    id_area = datoImpresora.id_area_id
                                    id_impresora = datoImpresora.id_impresora
                           
                                    marca = datoImpresora.marca
                                    modelo = datoImpresora.modelo
                                    
                                    
                                            
                                fecha = limpieza.fecha   
                                datosLimpiezas.append(["","","",marca,modelo, fecha])
         
        #Datos cartuchos    
        cartuchos = Cartuchos.objects.filter(cantidad=1)
        
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
      
        renovacionesActivas = []

        equiposActivos = Equipos.objects.filter(activo = "A")
        for equipo in equiposActivos:
            idActivo = equipo.id_equipo
            renovacionesTodas= Renovacion_Equipos.objects.all()
            for renovacion in renovacionesTodas:
                if idActivo == renovacion.id_equipo_id:
                    renovacionesActivas.append([renovacion.id_equipo_id, renovacion.fecha_compra, renovacion.fecha_renov])
        
        fecha = datetime.now()
        date = fecha.date()
        año = date.strftime("%Y") #2021
        mes = date.strftime("%m") #09
        
        equipos_año = []
        
        for equipo in renovacionesActivas:
            fecha_renovacion = equipo[2] #20 Octubre 2021    -     2021-10-22
            año_renovacion = fecha_renovacion.strftime("%Y")
            if año_renovacion == año:
                mes_renovacion = fecha_renovacion.strftime("%m") #10
                
                if mes_renovacion >= mes:
                    
                    resta = int(mes_renovacion) - int(mes)  #1
                
                    if resta >= 0 and resta <= 2:
                        id_equipo = equipo[0]
                        fecha_compra = equipo[1]
                        fecha_renovacion2 = equipo[2]
                        
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
            nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

            del request.session['recienIniciado']#se cierra la sesión del primer inicio de sesión

            recienIniciado = True
            cartuchosNoti = notificacionInsumos()
            mantenimientosNoti = notificacionLimpiezas()
            numeroNoti = numNoti()
            
            return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "recienIniciado":recienIniciado, "cantidades":cantidades, "datosLimpiezas":datosLimpiezas, 
                                                      "lista":lista, "baseDir":baseDir, "equipos_año":equipos_año, "impresoras_año":impresoras_año, "dia":dia, "mes_texto":mes_texto, "resta_dias":resta_dias, "año":año, "cartuchosNoti":cartuchosNoti
                                                      , "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        else:
            cartuchosNoti = notificacionInsumos()
            mantenimientosNoti = notificacionLimpiezas()
            numeroNoti = numNoti()
            return render(request, "Inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cantidades":cantidades, "datosLimpiezas":datosLimpiezas, 
                                                      "lista":lista, "baseDir":baseDir,"equipos_año":equipos_año, "impresoras_año":impresoras_año,  "dia":dia, "mes_texto":mes_texto, "resta_dias":resta_dias, "año":año ,"cartuchosNoti":cartuchosNoti
                                                      ,"mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def verAreas(request):
    
    if "idSesion" in request.session:

        estaEnVerAreas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        infoAreas = Areas.objects.all()
        
        cantidad_empleados = []
        
        for area in infoAreas:
            id_area_una = area.id_area
            areaInt = int(id_area_una)
            
            empleadosEnArea = Empleados.objects.filter(id_area_id__id_area = areaInt)#filtro de los empleados que esten dentro de un area especifica
            
            numero_empleados = 0
            for empleado in empleadosEnArea:
                numero_empleados+=1
            
            cantidad_empleados.append(numero_empleados)
            
        listaAreas = zip(infoAreas, cantidad_empleados)
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        return render(request, "Areas/verAreas.html", {"estaEnVerAreas":estaEnVerAreas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaAreas":listaAreas
                                                       , "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarAreas(request):
    
    if "idSesion" in request.session:

        estaEnAgregarAreas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        nombreCompleto = nombre + " " + apellidos
        
        
                
        #arreglo de nombres de clases que le dan color a un label
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
        #arreglo de nombres de colores
        nombresColores = ["Rojo", "Rosa", "Morado", "Indigo", "Azul", "Cyan", "Aqua", "Verde", "Verde bajo", "Verde Lima", "Amarillo", "Ambar", "Naranja", 
                        "Naranja Oscuro", "Cafe", "Gris", "Gris Azulado", "Negro"]
        
        #Obtener lista de colores en la table areas
        infoAreas = Areas.objects.all()
        
        coloresSi = []
        coloresNo = []
        
        for color in colores: 
            datosAreaCoincide = Areas.objects.filter(color=color[0])
            if datosAreaCoincide:
                coloresSi.append([color[0],color[1], color[2], color[3]] )
                
            else:
                coloresNo.append([color[0],color[1], color[2], color[3]])
                
        if request.method == "POST":
            area = request.POST['area']
            color = request.POST['colorElegido']
                  
            areaExiste = Areas.objects.filter(nombre= area)
            if areaExiste:
                errorExiste= True
                mensajeError = "El departamento " + area + " ya existe en la base de datos"
                
                return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "id_admin":id_admin,"arregloColores":colores, "nombresColores":nombresColores,
                "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, "error": errorExiste,
                "mensaje": mensajeError, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                registro = Areas(nombre=area, color=color)
                registro.save()
                guardadoExito = True
                mensajeExito = "El departamento " + area + " fue agregado exitosamente"
                

                return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas,"id_admin":id_admin, "arregloColores":colores, "nombresColores":nombresColores,
                "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, "guardado": guardadoExito,
                "mensaje": mensajeExito, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                

        return render(request,"Areas/agregarAreas.html", {"estaEnAgregarAreas": estaEnAgregarAreas, "id_admin":id_admin,"arregloColores":colores, "nombresColores":nombresColores, 
                                                          "infoAreas":infoAreas, "colorExiste": coloresSi, "colorInexistente": coloresNo, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def verEmpleados(request):
    
    if "idSesion" in request.session:

        estaEnVerEmpleados = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        empleadosActivos = Empleados.objects.filter(activo__icontains= "A", correo__icontains = "@customco.com.mx")
        empleadosInactivos = Empleados.objects.filter(activo__icontains= "I", correo__icontains = "@customco.com.mx")
        
        #empleados Actvos
        areasEnActivos = []
        datosAreasEnActivos = []
        
        for empleado in empleadosActivos:
            areasEnActivos.append(empleado.id_area_id)
            
        for id in areasEnActivos:
            datosArea = Areas.objects.filter(id_area = id) 
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnActivos.append([nombreArea, colorArea])
            
        lista = zip(empleadosActivos, datosAreasEnActivos)
        listaModal1 = zip(empleadosActivos, datosAreasEnActivos)
                    
        
        #empleadosInactivos
        areasEnInactivos = []
        datosAreasEnInactivos = []
        
        for empleado in empleadosInactivos:
            areasEnInactivos.append(empleado.id_area_id)
            
        for id in areasEnInactivos:
            areasInactivos = Areas.objects.filter(id_area = id)
                
            if areasInactivos:
                for dato in areasInactivos:
                    nombreArea = dato.nombre
                    colorArea = dato.color
                        
            datosAreasEnInactivos.append([nombreArea, colorArea])
                
        lista1 = zip(empleadosInactivos, datosAreasEnInactivos)
        listaModal2 = zip(empleadosInactivos, datosAreasEnInactivos)
        
        #Notificaciones altas y bajas
        if "idEmpleadoAlta" in request.session:
            alta = True
            mensaje = "Se dio de alta al empleado " + request.session['idEmpleadoAlta']
            del request.session["idEmpleadoAlta"]
            return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "alta":alta, "mensaje":mensaje, 
                                                                  "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2, "foto":foto})
        
        if "idEmpleadoBaja" in request.session:
            baja = True
            mensaje = "Se dio de baja al empleado " + request.session['idEmpleadoBaja']
            del request.session["idEmpleadoBaja"]
            return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "baja":baja, "mensaje":mensaje, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2
                                                                  , "foto":foto})
        
        if "textoCorreo" in request.session:
            correoEnviado = True
            mensaje = request.session['textoCorreo']
            del request.session["textoCorreo"]
            return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "correoEnviado":correoEnviado, "mensaje":mensaje, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2
                                                                  , "foto":foto})
        
        return render(request,"Empleados/verEmpleados.html", {"estaEnVerEmpleados": estaEnVerEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"lista1":lista1, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarEmpleados(request):


    if "idSesion" in request.session:
        
        estaEnAgregarEmpleados = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

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

            empleadoEnBd = False #booleano para ver si existe en la bd
            for empleado in lista_empleados:
                if empleado.apellidos == apellido_recibido and empleado.correo == correo_recibido:
                    empleadoEnBd = True #ya existe
            
            if empleadoEnBd == True:        
                yaExiste = True
                texto_error = "El empleado "+ nombre_recibido + " ya existe en la Base de Datos!"
                return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "yaExiste":yaExiste, "textoError":texto_error, "foto":foto})
            
            elif empleadoEnBd == False:
                noExiste = True
                if imagen_recibida == "":
                    registro = Empleados(nombre=nombre_recibido, apellidos=apellido_recibido, 
                        id_area = Areas.objects.get(id_area = area_recibida), puesto=puesto_recibido, correo = correo_recibido, contraseña=contra_recibida, activo = "A" )
                else:
                    registro = Empleados(nombre=nombre_recibido, apellidos=apellido_recibido, 
                        id_area = Areas.objects.get(id_area = area_recibida), puesto=puesto_recibido, correo = correo_recibido, contraseña=contra_recibida,imagen_empleado = imagen_recibida, activo = "A" )
                        
                    if registro:
                            
                        registro.save()
                            
                        datosEmpleado = Empleados.objects.filter(apellidos = apellido_recibido)
                            
                        for dato in datosEmpleado:
                            id_empleado_agregado = dato.id_empleado
                            
                        nombreCompletoEmp = nombre_recibido + " " + apellido_recibido
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                            
                        texto= "Se agregó al empleado " + nombreCompletoEmp 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Empleados", id_objeto=id_empleado_agregado, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
                           
                            
                        texto_existe = "El empleado "+ nombre_recibido + " fue agregado exitosamente!"
                        return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, "noExiste":noExiste, "textoExiste":texto_existe, 
                                                                                      "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                
        return render(request,"Empleados/agregarEmpleados.html", {"estaEnAgregarEmpleados": estaEnAgregarEmpleados, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "infoAreas":info_areas, 
                                                                  "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def verEquipos(request):


    if "idSesion" in request.session:
        
        estaEnVerEquipos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
                datosEmpleado = Empleados.objects.filter(id_empleado = id) #["1", "Sistemas", "rojo"]
                
                if datosEmpleado:
                    for dato in datosEmpleado:
                        nombreEmpleado = dato.nombre
                        apellidosEmpleado = dato.apellidos
                        areaEmpleado = dato.id_area_id
                        datosArea = Areas.objects.filter(id_area=areaEmpleado)
                        
                        if datosArea:
                            for dato in datosArea:
                                nombreArea = dato.nombre
                                color = dato.color
            
                datosAreasEnActivos.append([nombreEmpleado, apellidosEmpleado, nombreArea, color])
            
        lista = zip(equiposActivos, datosAreasEnActivos)
        lista2=zip(equiposActivos, datosAreasEnActivos)
        
        
        
        if "idEquipoBaja" in request.session:
            bajaEquipo=True
            if "errorBD" in request.session:
                bajaExito= "Error en la base de datos"
            else:
                bajaExito= "Se dió de baja el " + request.session["idEquipoBaja"] + " con éxito!"
            del request.session["idEquipoBaja"]
            return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "bajaEquipo":
                bajaEquipo, "bajaExito": bajaExito, "equiposInactivos":equiposInactivos, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "equiposActivos":equiposActivos, "lista2":lista2, "foto":foto})
            
        if "idEquipoAlta" in request.session:
            altaEquipo= True
            if "errorBD" in request.session:
                altaExito= "Error en la base de datos"
            else:
            
                altaExito= "Se dió de alta el " + request.session["idEquipoAlta"] + " con éxito"
            del request.session["idEquipoAlta"]
            return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,
                                                            "altaEquipo": altaEquipo, "altaExito":altaExito, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti,  "equiposActivos":equiposActivos, "lista2":lista2, "foto":foto})

        return render(request, "Equipos/verEquipos.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "equiposInactivos":equiposInactivos, 
                                                           "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti,  "equiposActivos":equiposActivos, "lista2":lista2, "foto":foto})

    else:
        return redirect('/login/') #redirecciona a url de inicio


def infoEquipo(request):
    
    if "idSesion" in request.session:
            
        estaEnVerEquipos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            
            idEquipo_recibido = request.POST['idEquipo']
            
            datosEquipo = Equipos.objects.filter(id_equipo=idEquipo_recibido)
            
            if datosEquipo:
            
                for datos in datosEquipo:
                    id_equipo= datos.id_equipo
                    propietario= datos.id_empleado_id
                    
                    sinPropietario = False
                    if propietario == None:
                        sinPropietario = True
                        
                        datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
                        for datos in datosRenovacion:
                            compra= datos.fecha_compra
                            renovar=  datos.fecha_renov
                        
                        #sinPropietario es true
                        
                        mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo=id_equipo)
                        if mantenimientos:
                            return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                            "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario, "mantenimientos":mantenimientos, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                        else:
                            return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                            "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})  
                    
                    else:
                        datosPropietario= Empleados.objects.filter(id_empleado=propietario)
                        for datos in datosPropietario:
                            idE = datos.id_empleado
                            nombre= datos.nombre
                            apellidos=datos.apellidos
                            nombreEmpleado= nombre + " " + apellidos
                            departamento=datos.id_area_id
                            datosDepa= Areas.objects.filter(id_area=departamento)
                            for datos in datosDepa:
                                nombreArea= datos.nombre
                                colorArea=datos.color
                                
                                
                        datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
                        for datos in datosRenovacion:
                            compra= datos.fecha_compra
                            renovar=  datos.fecha_renov
                            
                
                        #sinPropietario es falso
                        mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo=id_equipo)
                        mouses = Mouses.objects.filter(id_equipo = id_equipo)
                        teclados = Teclados.objects.filter(id_equipo = id_equipo)
                        monitores = Monitores.objects.filter(id_equipo = id_equipo)
                        telefonosE = Telefonos.objects.filter(id_empleado = idE)

                        

                        
                        
                       
                        if mouses or  mantenimientos or teclados or monitores or telefonosE:
                            return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                            "nombreEmpleado": nombreEmpleado, "nombreArea": nombreArea, "colorArea": colorArea, "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario,
                                                           "mouses":mouses,"mantenimientos":mantenimientos,"teclados":teclados,"monitores":monitores,"telefonosE":telefonosE, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                        else:
                            
                            return render(request, "Equipos/infoEquipo.html", {"estaEnVerEquipos": estaEnVerEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosEquipo":datosEquipo,
                                                            "nombreEmpleado": nombreEmpleado, "nombreArea": nombreArea, "colorArea": colorArea, "compra":compra, "renovar": renovar, "sinPropietario":sinPropietario, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                       

            else:
                
                noEncontro = True
                textoError = "No se encontró al equipo"
                
                return render (request, "Equipos/qrEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,"noEncontro":noEncontro, "textoError":textoError, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio        

def agregarEquipos(request):
    
    if "idSesion" in request.session:

        estaEnAgregarEquipos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
                                    estado=estado_recibida, activo="I",modelocargador = "Sin cargador")
                    if registroCompu:
                        registroCompu.save()
                        
                        registros = Equipos.objects.count()
                        
                        registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = registros), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                        registroAntiguiedad.save()
                        
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                        equipo= tipo_recibido + " " + marca_recibido + " " + modelo_recibida
                        texto= "Se agregó al equipo " + equipo 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=registros, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
                else:
                    registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                    color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                    memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                    estado=estado_recibida, activo="I", modelocargador = cargador_recibido)
                    if registroCompu:
                        registroCompu.save()
                        
                        registros = Equipos.objects.count()
                        
                        
                        
                        registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = registros), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                        registroAntiguiedad.save()
                        
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                        equipo= tipo_recibido + " " + marca_recibido + " " + modelo_recibida
                        texto= "Se agregó al equipo " + equipo 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=registros, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
                        
                compuSin = True
                textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " sin propietario!"
                return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "compuSin": compuSin, "textoCompu":textoCompu, 
                                                                      "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                
                
            elif propietario_recibida != "nopropietario":
                infoEmpleado = Empleados.objects.filter(id_empleado=propietario_recibida)
                
                for dato in infoEmpleado:
                    nombre = dato.nombre
                    
                compuCon= True
                textoCompu = "Se ha guardado "+tipo_recibido +" "+ marca_recibido + " " + modelo_recibida + " asignada al empleado " + nombre +"!"
                
                if cargador_recibido == "":
                    
                    registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                    color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                    memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                    id_empleado =Empleados.objects.get(id_empleado = propietario_recibida),estado=estado_recibida, activo="A", modelocargador = "Sin cargador")
                    if registroCompu:
                        registroCompu.save()
                        
                        ultimo_registro = Equipos.objects.count()
                        
                        
                        registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo = ultimo_registro), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                        registroAntiguiedad.save()
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                        equipo= tipo_recibido + " " + marca_recibido + " " + modelo_recibida
                        texto= "Se agregó al equipo " + equipo 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=ultimo_registro, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
                        
                else: 
                    registroCompu=Equipos(tipo=tipo_recibido,marca=marca_recibido,modelo= modelo_recibida,
                                    color=color_recibido,imagen= imagen_recibido, pdf=pdf_recibido,
                                    memoriaram=memoriaram_recibida,procesador=procesador_recibida,sistemaoperativo= sistemaop_recibida,
                                    id_empleado =Empleados.objects.get(id_empleado = propietario_recibida),estado=estado_recibida, activo="A", modelocargador = cargador_recibido)
                    if registroCompu:
                        registroCompu.save()
                        
                        registros = Equipos.objects.count()
                        
                        
                        
                        registroAntiguiedad = Renovacion_Equipos(id_equipo = Equipos.objects.get(id_equipo =  registros), fecha_compra = fecha_normal, fecha_renov = fecha_renovacion)
                        registroAntiguiedad.save()
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                        equipo= tipo_recibido + " " + marca_recibido + " " + modelo_recibida
                        texto= "Se agregó al equipo " + equipo 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto= registros, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
                        
                return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos ": estaEnAgregarEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "compuCon": compuCon, "textoCompu":textoCompu, 
                                                                      "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        
        if empleadosEquipo:
            
            for empleados in info_empleados:
                for emplEq in empleadosEquipo:
                    if empleados.id_empleado == emplEq.id_empleado_id:
                        empleadosiEq.append(empleados.id_empleado)
                    else:
                        empleadosnoEq.append([empleados.id_empleado,empleados.nombre,empleados.apellidos])
                        
            return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,"info_empleados":info_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        
        return render(request,"Equipos/agregarEquipos.html", {"estaEnAgregarEquipos": estaEnAgregarEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,"info_empleados": info_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def renovacionEquipos(request):
    if "idSesion" in request.session:
        
        estaEnRenovacionEquipos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
                    datosEmpleado= Empleados.objects.filter(id_empleado=int_propietario)
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
                    
            
        
        
        return render(request, "Equipos/renovacionEquipos.html", {"estaEnRenovacionEquipos": estaEnRenovacionEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosTabla":datosTabla, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def verImpresoras(request):
    
    if "idSesion" in request.session:

        estaEnVerImpresoras = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        
        impresorasActivas = Impresoras.objects.filter(activo__icontains= "A")
        impresorasInactivas = Impresoras.objects.filter(activo__icontains= "I")
        
        #impresoras Actvos
        areasEnActivos = []
        datosAreasEnActivos = []
        
        for impresoras in impresorasActivas:
            areasEnActivos.append(impresoras.id_area_id)
            #areasEnActivos = ["1"]
            
        for id in areasEnActivos:
            datosArea = Areas.objects.filter(id_area = id) #["1", "Sistemas", "rojo"]
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnActivos.append([nombreArea, colorArea])
            
        lista = zip(impresorasActivas, datosAreasEnActivos)
        listaModal1 = zip(impresorasActivas, datosAreasEnActivos)
        
        #impresoras inactivos
        areasEnInactivos = []
        datosAreasEnInactivos = []
        
        for impresoras in impresorasInactivas:
            areasEnInactivos.append(impresoras.id_area_id)
            #areasEnActivos = ["1"]
            
        for id in areasEnInactivos:
            datosArea = Areas.objects.filter(id_area= id) #["1", "Sistemas", "rojo"]
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnInactivos.append([nombreArea, colorArea])
            
        lista2 = zip(impresorasInactivas, datosAreasEnInactivos)
        listaModal2 = zip(impresorasInactivas, datosAreasEnInactivos)
        
        if "idImpresoraAlta" in request.session:
            alta = True
            mensaje = "Se dio de alta la impresora " + request.session['idImpresoraAlta']
            del request.session["idImpresoraAlta"]
            return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                            "lista2":lista2, "alta": alta, "mensaje": mensaje, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2, "foto":foto})
        if "idImpresoraBaja" in request.session:
            baja = True
            mensaje = "Se dio de baja la impresora " + request.session['idImpresoraBaja']
            del request.session["idImpresoraBaja"]
            return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                            "lista2":lista2, "baja": baja, "mensaje": mensaje, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2, "foto":foto})

        return render(request,"Impresoras/verImpresoras.html",{"estaEnVerImpresoras": estaEnVerImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista,
                                                            "lista2":lista2, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "listaModal1":listaModal1, "listaModal2":listaModal2, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def agregarImpresoras(request):
    
    if "idSesion" in request.session:

        estaEnAgregarImpresoras = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
                        
                        id_sistemas = request.session['idSesion']
                
                        fecha = datetime.now()
                        impresora= marca_recibido + " " + modelo_recibido
                        texto= "Se agregó la impresora " + impresora 
                        registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Impresoras", id_objeto=registros, operacion=texto, fecha_hora= fecha)
                        registroBitacora.save()
            
            impresoraAgregada = True
            
            impresoraExito= "La impresora " + marca_recibido + " " + modelo_recibido + " se guardó con éxito" 
            return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas,
                                                                        "impresoraAgregada":impresoraAgregada, "impresoraExito": impresoraExito, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        
        return render(request, "Impresoras/agregarImpresoras.html",{"estaEnAgregarImpresoras": estaEnAgregarImpresoras,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "info_areas": info_areas, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def renovacionImpresoras(request):
    
    if "idSesion" in request.session:
        
        estaEnRenovacionImpresoras = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
                datosArea= Areas.objects.filter(id_area=int_area)
                for datos in datosArea:
                    nombre= datos.nombre
                    color= datos.color
                    
            datosTabla.append([idImpresora, impresoraDatos, imagen, nombre, color, fechaCompra, fechaRenov])
        
        return render(request, "Impresoras/renovacionImpresoras.html", {"estaEnRenovacionImpresoras":estaEnRenovacionImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                                        "datosTabla":datosTabla, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def infoImpresora(request):
    if "idSesion" in request.session:
    
        estaEnVerImpresoras = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            
            idImpresora_recibido = request.POST['idImpresora']
            
            datosImpresora = Impresoras.objects.filter(id_impresora=idImpresora_recibido)
            
            
            listaAreas = []
            
            #Si encontró a una impresora
            if datosImpresora:
            
                for datos in datosImpresora:
                    id_impresora= datos.id_impresora
                    area= datos.id_area_id
                    
                    datosArea = Areas.objects.filter(id_area = area)
                    for dato in datosArea:
                        nombre = dato.nombre
                        color = dato.color
                        
                        listaAreas.append([nombre,color])

                    
                    datosRenovacion= Renovacion_Impresoras.objects.filter(id_impresora=id_impresora)
                    for datos in datosRenovacion:
                        compra= datos.fecha_compra
                        renovar=  datos.fecha_renov
                        
                    lista = zip(listaAreas, datosImpresora)
                    
                    cartuchos = Cartuchos.objects.filter(id_impresora_id__id_impresora = int(idImpresora_recibido))   
                    
                    return render(request, "Impresoras/infoImpresora.html", {"estaEnVerImpresoras": estaEnVerImpresoras, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosImpresora":datosImpresora,
                                                            "compra":compra, "renovar": renovar, "lista":lista, "cartuchos":cartuchos, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})  

            else:
                
                noEncontro = True
                textoError = "No se encontró la impresora"
                
                return render (request, "Impresoras/qrImpresora.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,"noEncontro":noEncontro, "textoError":textoError, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio   
    

def verInsumos(request):

    if "idSesion" in request.session:
        Insumos = True
        estaEnVerInsumos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        datosCartuchos = Cartuchos.objects.all()
        
        impresoras = []
        for cartuchos in datosCartuchos:
            idImpresora = cartuchos.id_impresora_id
            
            datosimpresoras = Impresoras.objects.filter(id_impresora=idImpresora)
            
        
            if datosimpresoras:
                for  datos in datosimpresoras:
                    marcaImpresora = datos.marca
                    modeloImpresora = datos.modelo
                
                    impresoras.append([marcaImpresora, modeloImpresora])
        lista = zip(datosCartuchos, impresoras)
        if "idInsumoActualizado" in request.session:
            insumoActualizado=True
            textoActualizado= request.session['idInsumoActualizado']
            del request.session["idInsumoActualizado"]
            
            return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "impresoras": impresoras, 
                                                        "datosCartuchos":datosCartuchos, "insumoActualizado":insumoActualizado, "textoActualizado":textoActualizado, "lista":lista, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})    
        
        return render(request, "Insumos/verInsumos.html",{"Insumos": Insumos, "estaEnVerInsumos":estaEnVerInsumos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "impresoras": impresoras, 
                                                      "datosCartuchos":datosCartuchos, "lista":lista, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def agregarInsumos(request):

    if "idSesion" in request.session:
        
        estaEnAgregarInsumos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        Insumos = True
        datosImpresoras = Impresoras.objects.filter(activo = "A")
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
            
            
            if registroInsumos:
                registroInsumos.save()
                ultimo_registro = Cartuchos.objects.count() #1
                        
                
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                cartucho= marca_recibido + " " + modelo_recibido
                texto= "Se agregó el insumo " + cartucho
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Insumos", id_objeto=ultimo_registro, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
                
            
                insumoAgregado = True
                
                insumoExito= "El insumo " + marca_recibido + " " + modelo_recibido + " se guardó con éxito" 
                return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                                "datosImpresoras":datosImpresoras, "insumoAgregado": insumoAgregado, "insumoExito": insumoExito, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            
        return render(request,"Insumos/agregarInsumos.html",{"estaEnAgregarInsumos": estaEnAgregarInsumos, "Insumos": Insumos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                            "datosImpresoras":datosImpresoras, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def actualizarInsumos(request):
    
    if "idSesion" in request.session:
    
        Insumos = True
        estaEnVerInsumos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        
        if request.method == "POST":
            
            id_cartucho_recibido = request.POST['idCartucho']
            cantida_recibida = request.POST['cantidadCartucho']
            
            datosCartucho = Cartuchos.objects.filter(id_cartucho=id_cartucho_recibido)
            
            for dato in datosCartucho:
                marca = dato.marca
                modelo = dato.modelo
                idimpresora = dato.id_impresora_id
                
            datosImpresora = Impresoras.objects.filter(id_impresora = idimpresora)
            
            for dato in datosImpresora:
                marcaImpresora = dato.marca
                modeloImpresora = dato.modelo
            
            actualizar = Cartuchos.objects.filter(id_cartucho=id_cartucho_recibido).update(cantidad=cantida_recibida)
            
            if actualizar:
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                cartucho= marca + " " + modelo
                texto= "Se editó el insumo " + cartucho + " a: " + cantida_recibida + " cartuchos." 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Insumos", id_objeto=id_cartucho_recibido, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
                
            
                textoCartucho = "Se ha actualizado el stock del cartucho "+marca+" "+modelo+" de la impresora "+marcaImpresora + " "+modeloImpresora +"!"
                    
                request.session['idInsumoActualizado'] = textoCartucho
            
            return redirect('/verInsumos/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def verProgramas(request):
    
    if "idSesion" in request.session:

        estaEnVerProgramas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        registrosProgramas = Programas.objects.all()
        
        if request.method == "POST":
            
            id_area_recibido = request.POST['idArea']
            
            datosArea = Areas.objects.filter(id_area=id_area_recibido)
            
            for dato in datosArea:
                nombreArea = dato.nombre
                colorArea = dato.color
            
            programasCasillas = []
            
            for programa in registrosProgramas:
                idPrograma = int(programa.id_programa)
                programaEncontrado = ProgramasArea.objects.filter(id_programa_id__id_programa=idPrograma) #(1,1), (1,6), (1,7)
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
                    
                        
                        
                    
            
            return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,
                                                                "registrosProgramas": registrosProgramas, "nombreArea": nombreArea, "colorArea":colorArea, "id_area_recibido":id_area_recibido, "lista": lista,
                                                                "n":n, "programaEncontrado":programaEncontrado, "areasPrograma":areasPrograma, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        

        return render(request,"Programas/verProgramas.html",{"estaEnVerProgramas": estaEnVerProgramas, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "registrosProgramas": registrosProgramas, 
                                                             "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarProgramas(request):
    
    if "idSesion" in request.session:

        estaEnAgregarProgramas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
            return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "registroExito": registroExito,
                                                                    "mensajeExito":mensajeExito, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            
            
        
        

        return render(request,"Programas/agregarProgramas.html",{"estaEnAgregarProgramas": estaEnAgregarProgramas, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def actualizarProgramasArea(request):
    
    if "idSesion" in request.session:
        
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        
        
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
                    programaGuardado = ProgramasArea.objects.filter(id_programa_id__id_programa=idPrograma) #(1,1), (1,6), (1,7)
                    
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
                    programaGuardado = ProgramasArea.objects.filter(id_programa_id__id_programa=idPrograma) #(1,1), (1,6), (1,7)
                    
                    areasPrograma=[]
                    
                    for area in programaGuardado:
                        areasPrograma.append(area.id_area_id)
                        
                        
                    if int(id_area_actualizar) in areasPrograma:
                        area = int(id_area_actualizar)
                        borrado = ProgramasArea.objects.get(id_area_id__id_area = area, id_programa_id__id_programa = idPrograma)
                        borrado.delete()
                        
                    else: #No esta esa área en la tabla, agregarlo
                        #no va aguardar nada
                        nada = True
            
            request.session["notificacion"] = "Se han actualizado los programas del area!"
            
            return redirect("/ProgramaPorArea/")   
                
        return redirect("/ProgramaPorArea/")
    
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def ProgramasporArea(request):
    
    if "idSesion" in request.session:

        estaEnverProgramasPorArea = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        areas = Areas.objects.all()
        
        cantidadProgramas=[]
        
        for area in areas:
            numeroDeProgramas = ProgramasArea.objects.filter(id_area_id = area.id_area).count #1
            if numeroDeProgramas:
                cantidadProgramas.append(numeroDeProgramas)
            else:
                cantidadProgramas.append("0")
                
        lista = zip(areas,cantidadProgramas)
            
        
                    
        if "notificacion" in request.session:
            
            noti = request.session["notificacion"]
            
            del request.session["notificacion"]
            
            siNoti = True
            
            
            
            return render(request,"Programas/verProgramasArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, 
                                                                 "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "noti":noti, "siNoti":siNoti, "foto":foto})            

        return render(request,"Programas/verProgramasArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, 
                                                                 "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def verProgramasPorArea(request):
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

        if request.method == "POST":
            
            nombreArea = request.POST['nombreArea']
            datosArea = Areas.objects.filter(nombre = nombreArea)
            
            for dato in datosArea:
                idArea = dato.id_area
                
            datosAreasProgramas = ProgramasArea.objects.filter(id_area_id = idArea)
            if datosAreasProgramas:
            
                arregloProgramas =[]
                
                for datos in datosAreasProgramas:
                    arregloProgramas.append(datos.id_programa_id)
                    
                arregloDatosProgramas = []
                arregloSistemasOperativos = []
                arregloMemoriasRAM = []
                arregloProcesadores = []
                
                
                
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
                        
                    arregloSistemasOperativos.append(sistemaoperativo)
                    arregloMemoriasRAM.append(memoria)
                    arregloProcesadores.append(procesador)
                    arregloDatosProgramas.append([id,nombre,tipo,licencia,idioma,sistemaoperativo,memoria,procesador,imagen])
                
                #nombreArea = Administracion

                estaEnverProgramasPorArea = True
                
                soBasico = ""
                soRecomendado = ""
                memoriaBasico = ""
                memoriaRecomendad = ""
                
                if "Windows 7 64 bit" in arregloSistemasOperativos:
                    soBasico = "Windows 7 64 bits"
                    soRecomendado = "Windows 8 64 bits"
                    
                if "Windows 8 64 bit" in arregloSistemasOperativos:
                    soBasico = "Windows 8 64 bits"
                    soRecomendado = "Windows 10 64 bits"
                
                if "Windows 10 64 bit" in arregloSistemasOperativos:
                    soBasico = "Windows 10 64 bits"
                    soRecomendado = "Windows 10 64 bits"
                    
                if "1 GB" in arregloMemoriasRAM:
                    memoriaBasico = "1 GB"
                    memoriaRecomendada = "2 GB"  
                       
                if "2 GB" in arregloMemoriasRAM:
                    memoriaBasico = "2 GB"
                    memoriaRecomendada = "4 GB" 
                       
                if "4 GB" in arregloMemoriasRAM:
                    memoriaBasico = "4 GB"
                    memoriaRecomendada = "8 GB"
                    
                if "8 GB" in arregloMemoriasRAM:
                    memoriaBasico = "8 GB"
                    memoriaRecomendada = "16 GB"
                    
                if "12 GB" in arregloMemoriasRAM:
                    memoriaBasico = "12 GB"
                    memoriaRecomendada = "16 GB"
                    
                if "16 GB" in arregloMemoriasRAM:
                    memoriaBasico = "16 GB"
                    memoriaRecomendada = "32 GB"
                    
                if "32 GB" in arregloMemoriasRAM:
                    memoriaBasico = "32 GB"
                    memoriaRecomendada = "64 GB"
                    
                procesadorMayor = 0
                velocidadesProcesadores = []
                for velocidad in arregloProcesadores:
                    velovidadSeparada = velocidad.split()
                    cont = 0
                    for x in velovidadSeparada:
                        cont = cont + 1
                        if cont == 1:
                            intVelocidad = float(x)
                            velocidadesProcesadores.append(intVelocidad)
                    
                contador = 0
                for vel in velocidadesProcesadores:
                    contador = contador + 1
                    if contador == 1:
                        procesadorMayor = vel
                    elif contador > 1:
                        if vel > procesadorMayor:
                            procesadorMayor = vel
                        
                intVel = float(procesadorMayor)
                velovidadRecomendada = intVel + .4   
                
            
                datosCompu = []
                datosCompu.append([soBasico, soRecomendado, memoriaBasico, memoriaRecomendada, str(procesadorMayor), str(velovidadRecomendada)])
                        
                    
                    
                
                
                return render(request, "Programas/tablaProgArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "id_admin":id_admin,"nombreArea":nombreArea, "nombreCompleto":nombreCompleto, "correo":correo, "idArea":idArea, "arregloDatosProgramas":arregloDatosProgramas, 
                                                                   "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "datosCompu":datosCompu})
            else:
                estaEnverProgramasPorArea = True
                return render(request, "Programas/tablaProgArea.html",{"estaEnverProgramasPorArea": estaEnverProgramasPorArea, "id_admin":id_admin,"nombreArea":nombreArea, "nombreCompleto":nombreCompleto, "correo":correo, "idArea":idArea, 
                                                                   "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def calendarioMant(request):

    if "idSesion" in request.session:
        
        estaEnCalendario = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        registroEquipos = CalendarioMantenimiento.objects.all()
        #propietarioCompu = Empleados.objects.all()
        #equipos= Equipos.objects.all()
        
        equipoPropietario = []
        impresoraArea = []
        fechasNuevas=[]
        for equipos in registroEquipos:
            if equipos.id_equipo_id != None :
                idEquipo =int (equipos.id_equipo_id)
                fecha= equipos.fecha
                operacion = equipos.operacion
        
                
            
                nueva_fecha = fecha + relativedelta(months=1)
                fechasNuevas.append(nueva_fecha)
        
                        
                
                
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
            else:
                
                idImpresora =int (equipos.id_impresora_id)
                fecha= equipos.fecha
                operacion = equipos.operacion
        
                
            
                nueva_fecha = fecha + relativedelta(months=1)
                fechasNuevas.append(nueva_fecha)
        
                        
                
                
                impresora = Impresoras.objects.filter(id_impresora=idImpresora)
                    
                for datosImpresora in impresora:
                    marca = datosImpresora.marca
                    modelo = datosImpresora.modelo
                    idArea = datosImpresora.id_area_id
                    
                    if idArea == None:
                        equipoPropietario.append(["Sin","departamento", marca,modelo])
                    else:
                        
                        datosArea= Areas.objects.filter(id_area = idArea)
                        
                        for area in datosArea:
                            idArea= int(area.id_area)
                            are = Areas.objects.filter(id_area= idArea)
                                
                            for datosA in are:
                                nombre= datosA.nombre
                         
                                
                        equipoPropietario.append([nombre,"", marca,modelo])
                
                
        lista = zip (registroEquipos, equipoPropietario, fechasNuevas)
        

        return render(request,"Mantenimiento/calendarioMant.html", {"estaEnCalendario": estaEnCalendario, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "registroEquipos":registroEquipos, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti
                                                                    , "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def formularioMant(request):
    
    if "idSesion" in request.session:
        
        estaEnFormulario = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        infoEquipos = Equipos.objects.filter(activo = "A")
        infoImpresoras = Impresoras.objects.filter(activo = "A")
        
        empleadosEquipo= []
        for empleado in infoEquipos:
            idEmpleado = empleado.id_empleado_id
            
            if idEmpleado == None:
                texto = "Sin propietario"
                empleadosEquipo.append([texto])

            else:
                empleados = Empleados.objects.filter(id_empleado = idEmpleado)

                for empleadoEquipo in empleados:
                    nombre = empleadoEquipo.nombre
                    apellidos = empleadoEquipo.apellidos
                    empleadosEquipo.append([nombre,apellidos])
            
        lista = zip(infoEquipos, empleadosEquipo)
    
        if request.method == "POST":
            
            equipo_recibido = request.POST['equipoProp']
            impresora_recibido = request.POST['impresora']
            operacion_recibido = request.POST['operacion']
            descripcion_recibida = request.POST['descripcion']
            fecha=datetime.now()
            
            if equipo_recibido != 'sinEquipo':
           
           
                        
                historialEquipo = CalendarioMantenimiento.objects.filter(id_equipo = equipo_recibido)
                        
                if historialEquipo: #Si al equipo ya se le realizó algo..
                    
                            
                
                    actualizacion = CalendarioMantenimiento.objects.filter(id_equipo =  equipo_recibido).update(fecha=fecha,  observaciones=descripcion_recibida)
                        
                    informacionEquipo = Equipos.objects.filter(id_equipo = equipo_recibido)
                
                    for equipoInf in informacionEquipo:
                        marca = equipoInf.marca
                        modelo = equipoInf.modelo
                        idEmpleado = equipoInf.id_empleado_id
                    
                    datosProp = Empleados.objects.filter(id_empleado = idEmpleado)
                    
                    for datosEm in datosProp:
                        nombreProp = datosEm.nombre
                        apellidosProp = datosEm.apellidos
                        
                    completoPropietario = nombreProp + " " + apellidosProp
                                
                    mantExito = True
                    mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "con propietario " + completoPropietario 
                                
                    return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                                                        "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti
                                                                                        , "foto":foto, "infoImpresoras":infoImpresoras})
                    
                registro = CalendarioMantenimiento(id_equipo=Equipos.objects.get(id_equipo=equipo_recibido), operacion=operacion_recibido, fecha=fecha, observaciones=descripcion_recibida)
                registro.save()
                
                equipos = Equipos.objects.filter(id_equipo = equipo_recibido)
                
                for equipo in equipos:
                    marca = equipo.marca
                    modelo = equipo.modelo
                
                mantExito = True
                mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "con propietario " + nombre + " " + apellidos
                
                return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                        "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "infoImpresoras":infoImpresoras})
            elif impresora_recibido != 'sinImpresora':
           
           
                        
                historialImpresora = CalendarioMantenimiento.objects.filter(id_impresora = impresora_recibido)
                        
                if historialImpresora: #Si al equipo ya se le realizó algo..
                    
                            
                
                    actualizacion = CalendarioMantenimiento.objects.filter(id_impresora =  impresora_recibido).update(fecha=fecha, observaciones=descripcion_recibida)
                        
                    informacionImpresora = Impresoras.objects.filter(id_impresora = impresora_recibido)
                
                    for impresoraInf in informacionImpresora:
                        marca = impresoraInf.marca
                        modelo = impresoraInf.modelo
                                
                    mantExito = True
                    mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "!!!"
                                
                    return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                                                        "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti
                                                                                        , "foto":foto, "infoImpresoras":infoImpresoras})
                    
                registro = CalendarioMantenimiento(id_impresora=Impresoras.objects.get(id_impresora=impresora_recibido), operacion=operacion_recibido, fecha=fecha, observaciones=descripcion_recibida)
                registro.save()
                
                informacionImpresora = Impresoras.objects.filter(id_impresora = impresora_recibido)
                
                for impresoraInf in informacionImpresora:
                    marca = impresoraInf.marca
                    modelo = impresoraInf.modelo
                                
                mantExito = True
                mensajeMant = "Se ha agregado el mantenimineto realizado a " + marca + " " + modelo + "!!!"
                
                return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, 
                                                                        "lista": lista, "mantExito":mantExito, "mensajeMant":mensajeMant, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "infoImpresoras":infoImpresoras})

        return render(request,"Mantenimiento/formularioMant.html",{"estaEnFormulario": estaEnFormulario, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, 
                                                                "lista": lista, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "infoImpresoras":infoImpresoras})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def verCarta(request):
    
    if "idSesion" in request.session:
        
        estaEnVerCarta = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
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
        
        
        
        
        return render(request,"cartaCompromiso/verCarta.html", {"estaEnVerCarta": estaEnVerCarta, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista1":lista1, 
                                                                "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def agregarCarta(request):
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        equipos= Equipos.objects.all()
        empledos=Empleados.objects.filter(activo="A", correo__icontains="@customco.com.mx")
        cartas= Carta.objects.all()
        fecha= datetime.now()
        areas=[]
        
        
        compusInactivas = Equipos.objects.filter(id_empleado__isnull=True, estado="Funcional", activo = "I")
        
        for empleado in empledos:
            idarea= int(empleado.id_area_id)
            nombreArea= Areas.objects.filter(id_area=idarea)
            
            for area in nombreArea:
                nombreAreas= area.nombre
                areas.append([nombreAreas])
                
        lista=zip(empledos,areas)

        if request.method == "POST":
            
            if request.POST['compuSeleccionada'] == "Ninguno":
                hayError = True
                error = "No hay computadora seleccionada disponible"
                return render(request, "cartaCompromiso/agregarCarta.html", {"hayError": hayError, "textoError":error})
            
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
            datosEquipo = Equipos.objects.filter(id_equipo = compuS)
        
            compuSeleccionada = True 
            compuSeleccionada2 = True
            empleadoDatos = Empleados.objects.filter(id_empleado=empleSeleccionado)
            
            for empleados in empleadoDatos:
                idArea= empleados.id_area_id
                
            datosArea = Areas.objects.filter(id_area=idArea)
            
            for area in datosArea:
                areaNombre= area.nombre
                color= area.color

            #Guardar datos en la tabla Carta de la base de datos

            estaEnAgregarCarta = True
            return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "equipos":equipos, "empleados": empledos, "lista":lista, "fecha":fecha,
                                                                    "compusInactivas": compusInactivas, "compuSeleccionada":compuSeleccionada,"compuSeleccionada2":compuSeleccionada2, "datosEquipo":datosEquipo, "empleadoDatos": empleadoDatos, "areaNombre": areaNombre, "color":color,
                                                                    "fecha": fecha, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        estaEnAgregarCarta = True
        return render(request, "cartaCompromiso/agregarCarta.html",{"estaEnAgregarCarta": estaEnAgregarCarta, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "equipos":equipos, "empleados": empledos, "lista":lista, "fecha":fecha,
                                                                 "compusInactivas": compusInactivas, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
        
    

    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def imprimirCarta(request):
    
    if "idSesion" in request.session:
    
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def BitacorasEquipos(request):
    
    if "idSesion" in request.session:
        
        estaEnEquiposBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        datosBitacora = Bitacora.objects.filter(tabla__icontains="Equipos")
        nombresUsuarios = []
        nombresEquipos=[]
        for dato in datosBitacora:
            id_user= dato.id_empleado_id
            
            datosEmpleados = Empleados.objects.filter(id_empleado = id_user)
            for empleado in datosEmpleados:
                idEmpl= empleado.id_empleado
                nombres = empleado.nombre
                apellido = empleado.apellidos
                
            nombreUsuario = str(idEmpl) + " - " + nombres + " " + apellido
            nombresUsuarios.append(nombreUsuario)
            
            idEntidad = int(dato.id_objeto)
            
            datosEquipo = Equipos.objects.filter(id_equipo=idEntidad)
            for equipo in datosEquipo:
                tipo = equipo.tipo
                marca = equipo.marca
                modelo = equipo.modelo
                idProp = equipo.id_empleado_id
                
                if idProp == None:
                    equipoCompleto = tipo + " " + marca + " " + modelo + " - sin propietario"
                else:
                    datosEmpleados = Empleados.objects.filter(id_empleado = idProp)
                    for empleado in datosEmpleados:
                        idEmpl= empleado.id_empleado
                        nombres = empleado.nombre
                        apellido = empleado.apellidos
                        
                    nombreProp = str(idEmpl) + " - " + nombres + " " + apellido
                    
                    equipoCompleto = tipo + " " + marca + " " + modelo + " " + nombreProp
                nombresEquipos.append(equipoCompleto)
        lista = zip(datosBitacora,nombresUsuarios, nombresEquipos)
        texto = "Bitácora de Equipos"
        
        return render(request, "Bitacora/Bitacoras.html",{"estaEnEquiposBitacora": estaEnEquiposBitacora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "texto": texto, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def BitacorasImpresoras(request):
    
    if "idSesion" in request.session:
        
        estaEnImpresorasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

        
        datosBitacora = Bitacora.objects.filter(tabla__icontains="Impresoras")
        nombresUsuarios = []
        nombresImpresoras=[]
        for dato in datosBitacora:
            id_user= dato.id_empleado_id
            
            datosEmpleados = Empleados.objects.filter(id_empleado = id_user)
            for empleado in datosEmpleados:
                idEmpl= empleado.id_empleado
                nombres = empleado.nombre
                apellido = empleado.apellidos
                
            nombreUsuario = str(idEmpl) + " - " + nombres + " " + apellido
            nombresUsuarios.append(nombreUsuario)
            
            idEntidad = int(dato.id_objeto)
            
            datosImpresora = Impresoras.objects.filter(id_impresora=idEntidad)
            for impresora in datosImpresora:
                idImp = impresora.id_impresora
                marca = impresora.marca
                modelo = impresora.modelo
                idDepa = impresora.id_area_id
                
                if idDepa == None:
                    impresoraCompleta = idImp + " " + marca + " " + modelo + " - sin departamento"
                else:
                    datosDepartamento = Areas.objects.filter(id_area = idDepa)
                    for departamento in datosDepartamento:
                        idDep= departamento.id_area
                        nombre = departamento.nombre
                        color = departamento.color
                        
                    nombreDepar = str(idDep) + " - " + nombre
                    
                    impresoraCompleta = marca + " " + modelo + " " + nombreDepar
                nombresImpresoras.append(impresoraCompleta)
        lista = zip(datosBitacora,nombresUsuarios, nombresImpresoras)
        texto = "Bitácora de Impresoras"
        

        return render(request, "Bitacora/Bitacoras.html",{"estaEnImpresorasBitacora": estaEnImpresorasBitacora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "texto":texto, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def BitacorasEmpleados(request):
    
    if "idSesion" in request.session:
        
        estaEnEmpleadosBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        datosBitacora = Bitacora.objects.filter(tabla__icontains="Empleados")
        nombresUsuarios = []
        nombresEmpleados=[]
        for dato in datosBitacora:
            id_user= dato.id_empleado_id
            
            datosEmpleados = Empleados.objects.filter(id_empleado = id_user)
            for empleado in datosEmpleados:
                idEmpl= empleado.id_empleado
                nombres = empleado.nombre
                apellido = empleado.apellidos
                
            nombreUsuario = str(idEmpl) + " - " + nombres + " " + apellido
            nombresUsuarios.append(nombreUsuario)
            
            idEntidad = int(dato.id_objeto)
            
            datosEmpleados = Empleados.objects.filter(id_empleado=idEntidad)
            for empleado in datosEmpleados:
                idEmpl = empleado.id_empleado
                nombres = empleado.nombre
                apellidos = empleado.apellidos
                idDepa = empleado.id_area_id
                
                if idDepa == None:
                    empleadoCompleta = nombres + " " + apellidos  + " - sin departamento"
                else:
                    datosDepartamento = Areas.objects.filter(id_area = idDepa)
                    for departamento in datosDepartamento:
                        idDep= departamento.id_area
                        nombre = departamento.nombre
                      
                        
                    nombreDepar = str(idDep) + " - " + nombre + " - "
                    
                    empleadoCompleta = nombreDepar + " " + nombres + " " + apellidos 
                nombresEmpleados.append(empleadoCompleta)
        lista = zip(datosBitacora,nombresUsuarios, nombresEmpleados)
        texto = "Bitácora de Empleados"
            
        return render(request, "Bitacora/Bitacoras.html",{"estaEnEmpleadosBitacora": estaEnEmpleadosBitacora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "texto":texto, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
def BitacorasCartuchos(request):
    
    if "idSesion" in request.session:
        
        estaEnCartuchosBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        datosBitacora = Bitacora.objects.filter(tabla__icontains="Insumos")
        nombresUsuarios = []
        nombresInsumos=[]
        for dato in datosBitacora:
            id_user= dato.id_empleado_id
            
            datosEmpleados = Empleados.objects.filter(id_empleado = id_user)
            for empleado in datosEmpleados:
                idEmpl= empleado.id_empleado
                nombres = empleado.nombre
                apellido = empleado.apellidos
                
            nombreUsuario = str(idEmpl) + " - " + nombres + " " + apellido
            nombresUsuarios.append(nombreUsuario)
            
            idEntidad = int(dato.id_objeto)
            
            datosCartuchos = Cartuchos.objects.filter(id_cartucho=idEntidad)
            for cartucho in datosCartuchos:
               
                marcas = cartucho.marca
                modelos = cartucho.modelo
                idImpre = cartucho.id_impresora_id
                
                
                datosImpresoras = Impresoras.objects.filter(id_impresora = idImpre)
                for impresora in datosImpresoras:
                    idIm= impresora.id_impresora
                    marca = impresora.marca
                    modelo = impresora.modelo
                      
                        
                    nombreImpres = str(idIm) + " - " + marca + " " + modelo +  " - "
                    
                    cartuchoCompleta = nombreImpres + " " + marcas + " " + modelos 
                nombresInsumos.append(cartuchoCompleta)
        lista = zip(datosBitacora,nombresUsuarios, nombresInsumos)
        texto = "Bitácora de Insumos"
        
        
        return render(request, "Bitacora/Bitacoras.html",{"estaEnCartuchosBitacora": estaEnCartuchosBitacora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "texto":texto, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    


def descargarPDF(request):
    if "idSesion" in request.session:
        
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def descargarPDF2(request):
    if "idSesion" in request.session:
        
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
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
    
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            equipoRecibido = request.POST['idEquipo']
            equipoDatos = Equipos.objects.filter(id_equipo=equipoRecibido)

            
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
                return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"ram": ram,"sistemasOperativos":sistemasOperativos, "equipoRecibido":equipoRecibido, "empleadosTotales":empleadosTotales, "sinPropietario":sinPropietario, 
                                                                    "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                empleado = Empleados.objects.filter(id_empleado=empleadoId)
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
                    
                        
                
            
                return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "ram": ram, "sistemasOperativos":sistemasOperativos, "empleado":empleado, "equipoRecibido":equipoRecibido, "datos_empleados":datos_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def editarEmpleado(request):
    
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

        if request.method == "POST":
            
            empleadoRecibido = request.POST['idEmpleadoEditar']
            
            datosEquipos = []
            equipo = Equipos.objects.filter(id_empleado_id__id_empleado = empleadoRecibido)
            for dato in equipo:
                id = dato.id_equipo
                tipo = dato.tipo
                marca = dato.marca
                modelo = dato.modelo
                imagen = dato.imagen
                
                equipoCompleto = "#" + str(id) +" - "+ tipo + " " + marca + " " + modelo
                
                datosEquipos.append([equipoCompleto, imagen])    
            
                
            
            
            
            datosEmpleadoEditar = Empleados.objects.filter(id_empleado = empleadoRecibido)
            
            if datosEmpleadoEditar:
                for datoEditar in datosEmpleadoEditar:
                
                    idareaEmpleado = datoEditar.id_area_id
                    
            datosArea = Areas.objects.filter(id_area= idareaEmpleado)
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
                    
            return render(request,"Editar/editarEmpleado.html", { "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "datosEmpleadoEditar": datosEmpleadoEditar, "nombreArea": nombreArea, "areasNuevas":areasNuevas, "datosEquipos":datosEquipos, 
                                                                 "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def editarEmpleadoBd(request):
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            
            nombreEditar = request.POST['nombreEditar']
            apellidoEditar = request.POST['apellidoEditar']
            areaEditar = request.POST['areaEditar']
            puestoEditar = request.POST['puestoEditar']
            correoEditar = request.POST['correoEditar']
            contraseñaEditar = request.POST['contraseñaEditar']
            
            areaInt = int(areaEditar)
            
            datosEmpleado = Empleados.objects.filter(correo = correoEditar)
            
            if datosEmpleado:
                for dato in datosEmpleado:
                    idEmpleado = dato.id_empleado
            
            actualizacion = Empleados.objects.filter(correo = correoEditar).update(nombre=nombreEditar, apellidos=apellidoEditar,
                                                                                            id_area=areaInt, puesto=puestoEditar, 
                                                                                            correo=correoEditar, contraseña=contraseñaEditar, 
                                                                                            )
            
            if actualizacion:
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                empleado= nombreEditar + " " + apellidoEditar 
                texto= "Se editó al empleado " + empleado 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Empleados", id_objeto=idEmpleado, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
            
            
                editado = True
                textoEdicion = "Se ha editado al empleado " + nombreEditar + " con éxito!"
                
                datosEmpleadoEditar = Empleados.objects.filter(id_empleado = idEmpleado)
                
                datosEquipos = []
                equipo = Equipos.objects.filter(id_empleado_id__id_empleado = idEmpleado)
                for dato in equipo:
                    id = dato.id_equipo
                    tipo = dato.tipo
                    marca = dato.marca
                    modelo = dato.modelo
                    imagen = dato.imagen
                    
                    equipoCompleto = "#" + str(id) +" - "+ tipo + " " + marca + " " + modelo
                    
                    datosEquipos.append([equipoCompleto, imagen])   
                
                if datosEmpleadoEditar:
                    for datoEditar in datosEmpleadoEditar:
                    
                        idareaEmpleado = datoEditar.id_area_id
                        
                datosArea = Areas.objects.filter(id_area = idareaEmpleado)
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
                        
                return render(request,"Editar/editarEmpleado.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "datosEmpleadoEditar": datosEmpleadoEditar, "nombreArea": nombreArea, "areasNuevas":areasNuevas, "editado":editado, "textoEdicion":textoEdicion, 
                                                                     "areaEditar":areaEditar, "datosEquipos":datosEquipos, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def editarEquipoBd(request):
    
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            equipoId = request.POST['idEquipo']
            ram_actualizar = request.POST['ram']
            propietario_actualizar = request.POST['propietario']
            sistema_actualizar = request.POST['sistema']
            estado_actualizar = request.POST['estado']
            cargador_actualizar = request.POST['cargador']

            
            if propietario_actualizar == "sinPropietario":
                actualizar = Equipos.objects.filter(id_equipo=equipoId).update(memoriaram=ram_actualizar, id_empleado_id=None,
                                                sistemaoperativo= sistema_actualizar, estado= estado_actualizar, modelocargador = cargador_actualizar, activo="I")
                
                
            elif propietario_actualizar !=  "sinPropietario": 
                int_empleado = int(propietario_actualizar)
                actualizar = Equipos.objects.filter(id_equipo=equipoId).update(memoriaram=ram_actualizar, id_empleado_id=Empleados.objects.get(id_empleado = int_empleado),
                                                sistemaoperativo= sistema_actualizar, estado= estado_actualizar, modelocargador = cargador_actualizar, activo="A")
            
            if actualizar:
               
                datos = Equipos.objects.filter(id_equipo = equipoId)
                
                for dato in datos:
                    tipo = dato.tipo
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoCompu = tipo + " " + marca + " " + modelo
                
                
                
                editado = True
                textoEdicion = "Se ha editado al equipo " + todoCompu + " con éxito!"
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=equipoId, operacion=textoEdicion, fecha_hora= fecha)
                registroBitacora.save()
                

                equipoRecibido = equipoId
                equipoDatos = Equipos.objects.filter(id_equipo=equipoRecibido)

                
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
                    return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"ram": ram,"sistemasOperativos":sistemasOperativos, "equipoRecibido":equipoRecibido, "empleadosTotales":empleadosTotales, "sinPropietario":sinPropietario, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    empleado = Empleados.objects.filter(id_empleado=empleadoId)
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
                        

                    return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "ram": ram, "sistemasOperativos":sistemasOperativos, "empleado":empleado, "equipoRecibido":equipoRecibido, "datos_empleados":datos_empleados, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                datos = Equipos.objects.filter(id_equipo = equipoId)
                
                for dato in datos:
                    tipo = dato.tipo
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoCompu = tipo + " " + marca + " " + modelo
                
                
                editado = True
                textoEdicion = "Error en la base de datos!"
               
             
                equipoRecibido = equipoId
                equipoDatos = Equipos.objects.filter(id_equipo=equipoRecibido)

                
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
                    return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"ram": ram,"sistemasOperativos":sistemasOperativos, "equipoRecibido":equipoRecibido, "empleadosTotales":empleadosTotales, "sinPropietario":sinPropietario, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    empleado = Empleados.objects.filter(id_empleado=empleadoId)
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
                        
                            
                    
                
                    return render(request, "Editar/editarEquipo.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "ram": ram, "sistemasOperativos":sistemasOperativos, "empleado":empleado, "equipoRecibido":equipoRecibido, "datos_empleados":datos_empleados, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    
        return render(request,"Editar/editarEmpleado.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def editarImpresoraBd(request):
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            impresora_id = request.POST['idImpresora']
            area_actualizar = request.POST['areaEditar']
            estado_actualizar = request.POST['estadoEditar']
            
            datosImpresora = Impresoras.objects.filter(id_impresora=impresora_id)
            
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
                    actualizar = Impresoras.objects.filter(id_impresora=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                                enred="N", ip="", activo = "A")
                else:
                    actualizar = Impresoras.objects.filter(id_impresoras=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                                enred="N", ip="", activo = "I")
            elif laVaAPonerEnRed == True:
                if estado_actualizar == "Funcional":
                    actualizar = Impresoras.objects.filter(id_impresora=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                                enred="S", ip=ip_actualizar, activo = "A")
                else:
                    actualizar = Impresoras.objects.filter(id_impresoras=impresora_id).update(id_area_id=area_actualizar, estado=estado_actualizar,
                                                enred="S", ip=ip_actualizar, activo = "I")
                    
                    
            if actualizar:
                
                
                datos_impresora = Impresoras.objects.filter(id_impresora = impresora_id)
                
                if datos_impresora:
                    for datoEditar in datos_impresora:
                    
                        idAreaImpresora = datoEditar.id_area_id
                        
                datosArea = Areas.objects.filter(id_area = idAreaImpresora)
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
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                impresora= marcaMostrar + " " + modeloMostrar
                texto= "Se editó la impresora " + impresora 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Impresoras", id_objeto=impresora_id, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
                return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datos_impresora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "nombreArea":nombreArea,
                                                                      "areasNuevas":areasNuevas, "editado":editado, "textoEditado":textoEditado, 
                                                                      "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        
        return render(request,"Editar/editarImpresora.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def altaEmpleado(request):
    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idAlta= request.POST['idEmpleadoAlta']
            
            datosEmpleado = Empleados.objects.filter(id_empleado = idAlta)
            
            for dato in datosEmpleado:
                nombre = dato.nombre
                apellido = dato.apellidos
                
            nombreCompletoEmp = nombre + " " + apellido
            
            actualizacion = Empleados.objects.filter(id_empleado = idAlta).update(activo = "A")
            if actualizacion:
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
    
                texto= "Se dió de alta al empleado " + nombreCompletoEmp 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Empleados", id_objeto=idAlta, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
            
                request.session['idEmpleadoAlta'] = nombreCompletoEmp
                
                return redirect('/verEmpleados/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaEmpleado(request):
    
    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idBaja= request.POST['idEmpleadoBaja']
            
            datosEmpleado = Empleados.objects.filter(id_empleado = idBaja)
            
            for dato in datosEmpleado:
                nombre = dato.nombre
                apellido = dato.apellidos
            
            nombreCompletoEmp = nombre + " " + apellido
            
            actualizacion = Empleados.objects.filter(id_empleado = idBaja).update(activo = "I")
            if actualizacion:
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
    
                texto= "Se dió de baja al empleado " + nombreCompletoEmp 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Empleados", id_objeto=idBaja, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
                
                request.session['idEmpleadoBaja'] = nombreCompletoEmp
                
                return redirect('/verEmpleados/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def altaImpresora(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":
        
            idAlta= request.POST['idImpresoraAlta']
            
            datosImpresora = Impresoras.objects.filter(id_impresora = idAlta)
            
            for dato in datosImpresora:
                marca = dato.marca
                modelo = dato.modelo
                
            nombreCompletoImp = marca + " " + modelo
            
            actualizacion = Impresoras.objects.filter(id_impresora = idAlta).update(activo = "A")
            
            if actualizacion: 
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
               
                texto= "Se dió de alta a la impresora" + nombreCompletoImp 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Impresoras", id_objeto=idAlta, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
            
            
                request.session['idImpresoraAlta'] = nombreCompletoImp
                
                return redirect('/verImpresoras/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaImpresora(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":
        
            idBaja= request.POST['idImpresoraBaja']
            
            datosImpresora = Impresoras.objects.filter(id_impresora = idBaja)
            
            for dato in datosImpresora:
                marca = dato.marca
                modelo = dato.modelo
            
            nombreCompletoImp = marca + " " + modelo
            
            actualizacion = Impresoras.objects.filter(id_impresora = idBaja).update(activo = "I")
            
            if actualizacion:
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
               
                texto= "Se dió de baja a la impresora" + nombreCompletoImp 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Impresoras", id_objeto=idBaja, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
            
                request.session['idImpresoraBaja'] = nombreCompletoImp
                
                return redirect('/verImpresoras/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def altaEquipo(request):
    
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            idAlta= request.POST['idEquipoAlta']
            
            datosEquipo = Equipos.objects.filter(id_equipo = idAlta)
            
            for dato in datosEquipo:
                marca = dato.marca
                modelo = dato.modelo
            
            equipo = marca + " " + modelo
            
            actualizacion = Equipos.objects.filter(id_equipo = idAlta).update(activo = "A")
            
            if actualizacion:
                
            
                request.session['idEquipoAlta'] = equipo
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                texto= "Se dio de alta al equipo " + equipo 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=idAlta, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()
            
                return redirect('/verEquipos/')
            else:
                
                request.session['idEquipoAlta'] = equipo
                request.session['errorBD'] = "Error en la base de datos"
                
                return redirect('/verEquipos/')
                
    else:
        return redirect('/login/') #redirecciona a url de inicio
  
def bajaEquipo(request):
    
    if "idSesion" in request.session:
        
        correo = request.session['correoSesion']
        if request.method == "POST":
            
            idBaja= request.POST['idEquipoBaja']
            
            datosEquipo = Equipos.objects.filter(id_equipo = idBaja)
            
            for dato in datosEquipo:
                marca = dato.marca
                modelo = dato.modelo
            
            equipo = marca + " " + modelo
            
            actualizacion = Equipos.objects.filter(id_equipo = idBaja).update(activo = "I", id_empleado_id = None)
            
            if actualizacion:
                
                id_sistemas = request.session['idSesion']
                
                fecha = datetime.now()
                texto= "Se dio de baja al equipo " + equipo 
                registroBitacora= Bitacora(id_empleado=Empleados.objects.get(id_empleado=id_sistemas), tabla = "Equipos", id_objeto=idBaja, operacion=texto, fecha_hora= fecha)
                registroBitacora.save()

                
                request.session['idEquipoBaja'] = equipo
                
            
                return redirect('/verEquipos/')
            else:
                request.session['idEquipoBaja'] = equipo
                request.session['errorBD'] = "Error en la base de datos"
                
                return redirect('/verEquipos/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
        

def editarImpresora(request):
    
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        if request.method == "POST":

            idImpresora= request.POST['idImpresoraEditar']
            datos_impresora = Impresoras.objects.filter(id_impresora = idImpresora)
            
            if datos_impresora:
                for datoEditar in datos_impresora:
                
                    idAreaImpresora = datoEditar.id_area_id
                    
            datosArea = Areas.objects.filter(id_area = idAreaImpresora)
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

            return render(request,"Editar/editarImpresora.html", {"impresoraAEditar":datos_impresora, "nombreCompleto":nombreCompleto, "correo":correo, "nombreArea":nombreArea, "areasNuevas":areasNuevas, 
                                                                  "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
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
        faltaFirma = True
            
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
            

        return render(request, "cartaCompromiso/firmarCarta.html", {"datosEquipo":datosEquipo, "datosEmpleado":datosEmpleado, "nombre":nombre, "color":color, "fecha":fecha,"faltaFirma":faltaFirma}) 
    

def reporteDepartamentos(request):
    
    if "idSesion" in request.session:
            
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Deparatmentos'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(380,750, "REPORTE DEPARTAMENTOS")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
            
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
            
        c.drawString(180,660, 'Reporte Departamentos')
        
        #obtener datos de area
        
        datosAreas= Areas.objects.all()
        cantidad_empleados = []
        
        for area in datosAreas:
            id_area_una = area.id_area
            areaInt = int(id_area_una)
            
            empleadosEnArea = Empleados.objects.filter(id_area_id__id_area = areaInt)
            
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def reporteEmpleadosActivos(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":

            activo= request.POST['activo'] #A o I
            
            
        
        empleaditos = Empleados.objects.filter(activo__icontains = activo, correo__icontains = "customco.com.mx") #20 empleados
        
        numero_empleados = 0 #contador
        for empleado in empleaditos:
            numero_empleados +=1 #20
            
        if numero_empleados == 0:
            numero_empleados =1
        
        division = numero_empleados // 9 #Resultado 2, a fuerzas va a haber 2 hojas en el pdf
        residuo = numero_empleados%9 #residuo hay 2
        
        
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 3
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Empleados'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        contadorEmpleados = 0
        contadorHojas = 1
        for hoja in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            datosEmpleados= Empleados.objects.filter(activo__icontains=activo, correo__icontains = "customco.com.mx") ##11 empleados
            
            
            ids =[]
            nombres = []
            apellidos = []
            areas = []
            puestos = []
            correos = []
            contras = []
            urls_imagenes = []
            base_dir = str(settings.BASE_DIR) #C:\Users\Sistemas\Desktop\Custom System\Custom-System\djangoCS
            
            if contadorHojas == 4:
                contadorEmpelados4 = 0
                contadorEmpleadosxHoja = 0
                for empleado in datosEmpleados:
                    contadorEmpelados4 += 1
                    if contadorEmpelados4 > 27 and contadorEmpelados4 <=36:
                        contadorEmpleadosxHoja +=1
                        
                        #Obtener solo empleados que quepan en la hoja
                        idarea = empleado.id_area_id
                        imagen = empleado.imagen_empleado
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        
                        urls_imagenes.append(img)
                        
                        info_area = Areas.objects.filter(id_area = idarea)
                        
                        for dato in info_area:
                            nombre = dato.nombre
                            areas.append(nombre)
                        
                        ids.append(str(empleado.id_empleado))
                        nombres.append(empleado.nombre)
                        apellidos.append(empleado.apellidos)
                        puestos.append(empleado.puesto)
                        correos.append(empleado.correo)
                        contras.append(empleado.contraseña)
                    
                        
                        contadorEmpleados += 1 #11
  
                    
                listaEmpleados = zip(ids, nombres, apellidos, areas, puestos, correos, contras, urls_imagenes)
                contadorHojas = 4
                if contadorEmpleadosxHoja == 9:
                    high = 600 - ((contadorEmpleadosxHoja+1) * 33)
                else:
                    high = 600 - (contadorEmpleadosxHoja * 33)
            
            if contadorHojas == 3:
                contadorEmpelados3 = 0
                contadorEmpleadosxHoja = 0
                for empleado in datosEmpleados:
                    contadorEmpelados3 += 1
                    if contadorEmpelados3 > 18 and contadorEmpelados3 <=27:
                        contadorEmpleadosxHoja +=1
                        
                        #Obtener solo empleados que quepan en la hoja
                        idarea = empleado.id_area_id
                        imagen = empleado.imagen_empleado
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        
                        urls_imagenes.append(img) #Imagen del empleado
                        
                        info_area = Areas.objects.filter(id_area = idarea)
                        
                        for dato in info_area:
                            nombre = dato.nombre
                            areas.append(nombre)
                        
                        ids.append(str(empleado.id_empleado))
                        nombres.append(empleado.nombre)
                        apellidos.append(empleado.apellidos)
                        puestos.append(empleado.puesto)
                        correos.append(empleado.correo)
                        contras.append(empleado.contraseña)
                    
                        
                        contadorEmpleados += 1 #11

                listaEmpleados = zip(ids, nombres, apellidos, areas, puestos, correos, contras, urls_imagenes)
                contadorHojas = 4
                if contadorEmpleadosxHoja == 9:
                    high = 600 - ((contadorEmpleadosxHoja+1) * 33)
                else:
                    high = 600 - (contadorEmpleadosxHoja * 33)

            
            if contadorHojas == 2:
                contadorEmpelados2 = 0
                contadorEmpleadosxHoja = 0
                for empleado in datosEmpleados:
                    contadorEmpelados2 += 1
                    if contadorEmpelados2 > 9 and contadorEmpelados2 <=18:
                        contadorEmpleadosxHoja +=1
                        
                        #Obtener solo empleados que quepan en la hoja
                        idarea = empleado.id_area_id
                        imagen = empleado.imagen_empleado
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        
                        urls_imagenes.append(img)
                        
                        info_area = Areas.objects.filter(id_area = idarea)
                        
                        for dato in info_area:
                            nombre = dato.nombre
                            areas.append(nombre)
                        
                        ids.append(str(empleado.id_empleado))
                        nombres.append(empleado.nombre)
                        apellidos.append(empleado.apellidos)
                        puestos.append(empleado.puesto)
                        correos.append(empleado.correo)
                        contras.append(empleado.contraseña)
                    

                listaEmpleados = zip(ids, nombres, apellidos, areas, puestos, correos, contras, urls_imagenes)
                contadorHojas = 3
                if contadorEmpleadosxHoja == 9:
                    high = 600 - ((contadorEmpleadosxHoja+1) * 33)
                else:
                    high = 600 - (contadorEmpleadosxHoja * 33)

            if contadorHojas == 1:
                contadorEmpleadosxHoja1 = 0
                for empleado in datosEmpleados:
                    
                    contadorEmpleados += 1 #10
                    
                    
                    if contadorEmpleados <= 9:
                        #Obtener solo empleados que quepan en la hoja
                        idarea = empleado.id_area_id
                        imagen = empleado.imagen_empleado
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        
                        urls_imagenes.append(img)
                        
                        info_area = Areas.objects.filter(id_area = idarea)
                        
                        for dato in info_area:
                            nombre = dato.nombre
                            areas.append(nombre)
                            
                        ids.append(str(empleado.id_empleado))
                        nombres.append(empleado.nombre)
                        apellidos.append(empleado.apellidos)
                        puestos.append(empleado.puesto)
                        correos.append(empleado.correo)
                        contras.append(empleado.contraseña)
                        contadorEmpleadosxHoja1 +=1

                #solo 9 empleados
                listaEmpleados = zip(ids, nombres, apellidos, areas, puestos, correos, contras, urls_imagenes)
                contadorHojas = 2
                if contadorEmpleadosxHoja1 == 9:
                    high = 600 - ((contadorEmpleadosxHoja1+1) * 33)
                else:
                    high = 600 - (contadorEmpleadosxHoja1 * 33)
                

            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            if activo == "A":
                c.drawString(360,750, "REPORTE EMPLEADOS ACTIVOS")
            elif activo == "I":
                c.drawString(360,750, "REPORTE EMPLEADOS INACTIVOS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            if activo == "A":
                c.drawString(150,660, 'Reporte Empleados Activos')
            elif activo == "I":
                c.drawString(150,660, 'Reporte Empleados Inactivos')
            

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
            filasTabla=[]
            filasTabla.append([id_empleado, nombre, apellido, imagen, departamento, puesto, correo])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
     
            
            for id, nombre, apellido, areas, puesto, correo, contra, imagenes in listaEmpleados:
                campo_empleado = Paragraph(id, styleN)
                campo_nombre = Paragraph(nombre, styleN)
                campo_apellidos = Paragraph(apellido, styleN)
                campo_area = Paragraph(areas, styleN)
                campo_puesto = Paragraph(puesto, styleN)
                campo_correo = Paragraph(correo, styleN)
                campo_contraseña = Paragraph(contra, styleN)
                
                fila = [campo_empleado, campo_nombre, campo_apellidos, imagenes, campo_area, campo_puesto, campo_correo, 
                        ]
                filasTabla.append(fila)
                
                high= high - 18 
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[1 * cm, 2 * cm, 3 * cm, 2.25 * cm, 2 * cm, 4 * cm, 4 * cm])
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
            tabla.drawOn(c, 40, high)
            
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def reporteRenovacionEq(request):
    
    if "idSesion" in request.session:
    
    
        renovacionEquipos = Renovacion_Equipos.objects.all()
        
        numero_equipos = 0 #contador
        for equipo in renovacionEquipos:
            numero_equipos +=1 #20
            
        if numero_equipos == 0:
            numero_equipos =1
        
        division = numero_equipos // 30 #Resultado 2, a fuerzas va a haber 2 hojas en el pdf
        residuo = numero_equipos%30 #residuo hay 2
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 3
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte renovación de equipos'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        
        contadorHojas = 1
        for hoja in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            renovacionEquipos = Renovacion_Equipos.objects.all()
            
            
            ids =[]
            equiposRe = []
            propietarios = []
            departamentos = []
            compras = []
            renovaciones = []

            if contadorHojas == 3:
                contadorEquipos = 0
                contadorEquiposxHoja = 0
                for datosRenovacion in renovacionEquipos:
                    
                    contadorEquipos += 1 #10
                    
                    
                    if contadorEquipos > 48 and contadorEquipos <=72:
                        #Obtener solo empleados que quepan en la hoja
                        idRenovacion= datosRenovacion.id_renov_equipo
                        equipo= datosRenovacion.id_equipo_id
                        compra= datosRenovacion.fecha_compra
                        renovacion = datosRenovacion.fecha_renov
                        
                        ids.append(idRenovacion)
                        compras.append(compra)
                        renovaciones.append(renovacion)
                        
                        equipos = Equipos.objects.filter(id_equipo=equipo)
                        for datosEquipo in equipos:
                            tipo = datosEquipo.tipo
                            marca = datosEquipo.marca
                            modelo = datosEquipo.modelo
                            col= datosEquipo.color
                            propietario = datosEquipo.id_empleado_id
                            datosEquipos = tipo + "" + marca + "" + modelo + "" + col
                            equiposRe.append(datosEquipos)
                            
                            if propietario == None:
                                datosPropietario = "Sin propietario"
                                area = "Sin departamento"
                            else:
                                
                                propietarios = Empleados.objects.filter(id_empleado = propietario)
                                for datosProp in propietarios:
                                    nombres = datosProp.nombre
                                    apellidos = datosProp.apellidos
                                    depa = datosProp.id_area_id
                                    datosPropietario= nombres + "" + apellidos
                            
                                departamentos = Areas.objects.filter(id_area = depa)
                                for datosArea in departamentos:
                                    area = datosArea.nombre
                                    color = datosArea.color
                            propietarios.append(datosPropietario)
                            departamentos.append(area)
                        contadorEquiposxHoja +=1
                    
 
                #solo 9 empleados
                listaEquipos = zip(ids, equiposRe, propietarios, departamentos, compras, renovaciones )
                contadorHojas = 4
                if contadorEquiposxHoja == 24:
                    high = 600 - ((contadorEquiposxHoja+1) * 4)
                else:
                    high = 600 - (contadorEquiposxHoja * 1)

            if contadorHojas == 2:
                contadorEquipos = 0
                contadorEquiposxHoja = 0
                for datosRenovacion in renovacionEquipos:
                    
                    contadorEquipos += 1 #10
                    
                    
                    if contadorEquipos > 24 and contadorEquipos <= 48:
                        #Obtener solo empleados que quepan en la hoja
                        idRenovacion= datosRenovacion.id_renov_equipo
                        equipo= datosRenovacion.id_equipo_id
                        compra= datosRenovacion.fecha_compra
                        renovacion = datosRenovacion.fecha_renov
                        
                        ids.append(idRenovacion)
                        compras.append(compra)
                        renovaciones.append(renovacion)
                        
                        equipos = Equipos.objects.filter(id_equipo=equipo)
                        for datosEquipo in equipos:
                            tipo = datosEquipo.tipo
                            marca = datosEquipo.marca
                            modelo = datosEquipo.modelo
                            col= datosEquipo.color
                            propietario = datosEquipo.id_empleado_id
                            datosEquipos = tipo + "" + marca + "" + modelo + "" + col
                            equiposRe.append(datosEquipos)
                            
                            if propietario == None:
                                datosPropietario = "Sin propietario"
                                area = "Sin departamento"
                            else:
                                
                                propietariosx = Empleados.objects.filter(id_empleado = propietario)
                                for datosProp in propietariosx:
                                    nombres = datosProp.nombre
                                    apellidos = datosProp.apellidos
                                    depa = datosProp.id_area_id
                                    datosPropietario= nombres + "" + apellidos
                            
                                departamentosx = Areas.objects.filter(id_area = depa)
                                for datosArea in departamentosx:
                                    area = datosArea.nombre
                                    color = datosArea.color
                            propietarios.append(datosPropietario)
                            departamentos.append(area)
                        contadorEquiposxHoja +=1
   
                    
                #solo 9 empleados
                listaEquipos = zip(ids, equiposRe, propietarios, departamentos, compras, renovaciones )
                contadorHojas = 3
                if contadorEquiposxHoja == 24:
                    high = 600 - ((contadorEquiposxHoja+1) * 4)
                else:
                    high = 600 - (contadorEquiposxHoja * 1)
            
        
            if contadorHojas == 1:
                contadorEquipos = 0
                contadorEquiposxHoja = 0
                
                for datosRenovacion in renovacionEquipos:
                    contadorEquipos += 1 #10
    
                    if contadorEquipos <= 24:
                        #Obtener solo empleados que quepan en la hoja
                        idRenovacion= datosRenovacion.id_renov_equipo
                        equipo= datosRenovacion.id_equipo_id
                        compra= datosRenovacion.fecha_compra
                        renovacion = datosRenovacion.fecha_renov
                            
                        ids.append(idRenovacion)
                        compras.append(compra)
                        renovaciones.append(renovacion)
                            
                        equipos = Equipos.objects.filter(id_equipo=equipo)
                            
                        for datosEquipo in equipos:
                            tipo = datosEquipo.tipo
                            marca = datosEquipo.marca
                            modelo = datosEquipo.modelo
                            col= datosEquipo.color
                            propietario = datosEquipo.id_empleado_id
                            datosEquipos = tipo + "" + marca + "" + modelo + "" + col
                            equiposRe.append(datosEquipos)
                                
                            if propietario == None:
                                datosPropietario = "Sin propietario"
                                area = "Sin departamento"
                            else:
                                    
                                propietariosx = Empleados.objects.filter(id_empleado = propietario)
                                for datosProp in propietariosx:
                                    nombres = datosProp.nombre
                                    apellidos = datosProp.apellidos
                                    depa = datosProp.id_area_id
                                    datosPropietario= nombres + "" + apellidos
                                
                                departamentosx = Areas.objects.filter(id_area = depa)
                                for datosArea in departamentosx:
                                    area = datosArea.nombre
                                    color = datosArea.color
                            propietarios.append(datosPropietario)
                            departamentos.append(area)
                        contadorEquiposxHoja +=1
                    
                    #solo 9 empleados
                    listaEquipos = zip(ids, equiposRe, propietarios, departamentos, compras, renovaciones )
                    contadorHojas = 2
                    if contadorEquiposxHoja == 24:
                        high = 600 - ((contadorEquiposxHoja+1) * 4)
                    else:
                        high = 600 - (contadorEquiposxHoja *1)

            base_dir = str(settings.BASE_DIR)
            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(360,750, "REPORTE RENOVACIÓN EQUIPOS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            c.drawString(150,660, 'Reporte Renovación Equipos')
            

            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_renovacion = Paragraph('''ID''', styleBH)
            equipo_re = Paragraph('''Equipo''', styleBH)
            propietario_re = Paragraph('''Propietario''', styleBH)
            departamento_re = Paragraph('''Departamento''', styleBH)
            compra_re = Paragraph('''Fecha Compra.''', styleBH)
            renovacion_re = Paragraph('''Fecha Renovación''', styleBH)
            
            filasTabla=[]
            filasTabla.append([id_renovacion,equipo_re, propietario_re, departamento_re, compra_re, renovacion_re ])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            

            for id_re, equipo, propietario, departamento, compra, renov in listaEquipos:
                campo_id = Paragraph(str(id_re), styleN)
                campo_equipo = Paragraph(str(equipo), styleN)
                campo_propietario = Paragraph(str(propietario), styleN)
                campo_departamento = Paragraph(str(departamento), styleN)
                campo_compra = Paragraph(str(compra), styleN)
                campo_renovacion = Paragraph(str(renov), styleN)
            
                
                fila = [campo_id, campo_equipo, campo_propietario, campo_departamento, campo_compra, campo_renovacion]
                filasTabla.append(fila)
                
                high= high - 18 
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[1 * cm, 5 * cm, 4 * cm, 3 * cm, 3 * cm, 3 * cm])
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
            tabla.drawOn(c, 35, high)
            
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
            
            
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta
    else:
        return redirect('/login/') #redirecciona a url de inicio     
    
def reporteEquiposActivos(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":

            activo= request.POST['activo']
            
            
        
        equipitos = Equipos.objects.filter(activo__icontains = activo) #11 empleados
        
        numero_equipos = 0
        for equipo in equipitos:
            numero_equipos +=1
            
        if numero_equipos == 0:
            numero_equipos =1
        
        division = numero_equipos // 9 #Resultado 1, sin residuo
        residuo = numero_equipos%9 #residuo hay 2
        
        
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Equipos'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        contadorEquipos = 0
        contadorHojas = 1
        for hoja2 in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            datosEquipos= Equipos.objects.filter(activo__icontains=activo) ##1 equipo
            
            
            ids =[]
            tipos = []
            marcas = []
            modelos = []
            colores = []
            memorias = []
            procesadores = []
            sistemas = []
            procesadores = []
            cargadores = []
            propietarios = []
            estados = []
            urls_imagenes = []
            base_dir = str(settings.BASE_DIR)
            
            if contadorHojas == 5:
                contadorEquipos = 0
                contadorEquiposXHoja = 0
                for equipo in datosEquipos:
                    
                    contadorEquipos += 1 #10
                    if contadorEquipos > 36 and contadorEquipos <=45:
                        imagen = equipo.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idempleado = equipo.id_empleado_id
                        if idempleado == None:
                            propietarios.append("Sin propietario")
                        else:
                            info_empleado = Empleados.objects.filter(id_empleado = idempleado)
                            
                            for dato in info_empleado:
                                nombre = dato.nombre
                                apellidos = dato.apellidos
                                nombre_completo = nombre + " " + apellidos
                                propietarios.append(nombre_completo)
                            
                        ids.append(str(equipo.id_equipo))
                        tipos.append(equipo.tipo)
                        marcas.append(equipo.marca)
                        modelos.append(equipo.modelo)
                        colores.append(equipo.color)
                        memorias.append(equipo.memoriaram)
                        procesadores.append(equipo.procesador)
                        sistemas.append(equipo.sistemaoperativo)
                        cargadores.append(equipo.modelocargador)
                        estados.append(equipo.estado)
                        
                        
                        contadorEquiposXHoja +=1
                        
                    
                #solo 9 empleados
                listaEquipos = zip(ids, tipos, marcas, modelos, colores, memorias, procesadores, sistemas, cargadores, estados, propietarios, urls_imagenes)
                
                contadorHojas = 6
                if contadorEquiposXHoja == 9:
                    high = 600 - ((contadorEquiposXHoja+1) * 33)
                else:
                    high = 600 - (contadorEquiposXHoja * 33)
            
            if contadorHojas == 4:
                contadorEquipos = 0
                contadorEquiposXHoja = 0
                for equipo in datosEquipos:
                    
                    contadorEquipos += 1 #10
                    if contadorEquipos > 27 and contadorEquipos <=36:
                        imagen = equipo.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idempleado = equipo.id_empleado_id
                        if idempleado == None:
                            propietarios.append("Sin propietario")
                        else:
                            info_empleado = Empleados.objects.filter(id_empleado = idempleado)
                            
                            for dato in info_empleado:
                                nombre = dato.nombre
                                apellidos = dato.apellidos
                                nombre_completo = nombre + " " + apellidos
                                propietarios.append(nombre_completo)
                            
                        ids.append(str(equipo.id_equipo))
                        tipos.append(equipo.tipo)
                        marcas.append(equipo.marca)
                        modelos.append(equipo.modelo)
                        colores.append(equipo.color)
                        memorias.append(equipo.memoriaram)
                        procesadores.append(equipo.procesador)
                        sistemas.append(equipo.sistemaoperativo)
                        cargadores.append(equipo.modelocargador)
                        estados.append(equipo.estado)
                        
                        
                        contadorEquiposXHoja +=1
                        
                    
                #solo 9 empleados
                listaEquipos = zip(ids, tipos, marcas, modelos, colores, memorias, procesadores, sistemas, cargadores, estados, propietarios, urls_imagenes)
                
                contadorHojas = 5
                if contadorEquiposXHoja == 9:
                    high = 600 - ((contadorEquiposXHoja+1) * 33)
                else:
                    high = 600 - (contadorEquiposXHoja * 33)
                    
                    
            
            if contadorHojas == 3:
                contadorEquipos = 0
                contadorEquiposXHoja = 0
                for equipo in datosEquipos:
                    
                    contadorEquipos += 1 #10
                    if contadorEquipos > 18 and contadorEquipos <=27:
                        imagen = equipo.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idempleado = equipo.id_empleado_id
                        if idempleado == None:
                            propietarios.append("Sin propietario")
                        else:
                            info_empleado = Empleados.objects.filter(id_empleado = idempleado)
                            
                            for dato in info_empleado:
                                nombre = dato.nombre
                                apellidos = dato.apellidos
                                nombre_completo = nombre + " " + apellidos
                                propietarios.append(nombre_completo)
                            
                        ids.append(str(equipo.id_equipo))
                        tipos.append(equipo.tipo)
                        marcas.append(equipo.marca)
                        modelos.append(equipo.modelo)
                        colores.append(equipo.color)
                        memorias.append(equipo.memoriaram)
                        procesadores.append(equipo.procesador)
                        sistemas.append(equipo.sistemaoperativo)
                        cargadores.append(equipo.modelocargador)
                        estados.append(equipo.estado)
                        
                        
                        contadorEquiposXHoja +=1
                        
                    
                #solo 9 empleados
                listaEquipos = zip(ids, tipos, marcas, modelos, colores, memorias, procesadores, sistemas, cargadores, estados, propietarios, urls_imagenes)
                
                contadorHojas = 4
                if contadorEquiposXHoja == 9:
                    high = 600 - ((contadorEquiposXHoja+1) * 33)
                else:
                    high = 600 - (contadorEquiposXHoja * 33)
                    
                    
            
            if contadorHojas == 2:
                contadorEquipos = 0
                contadorEquiposXHoja = 0
                for equipo in datosEquipos:
                    
                    contadorEquipos += 1 #10
                    if contadorEquipos > 9 and contadorEquipos <=18:
                        imagen = equipo.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idempleado = equipo.id_empleado_id
                        if idempleado == None:
                            propietarios.append("Sin propietario")
                        else:
                            info_empleado = Empleados.objects.filter(id_empleado = idempleado)
                            
                            for dato in info_empleado:
                                nombre = dato.nombre
                                apellidos = dato.apellidos
                                nombre_completo = nombre + " " + apellidos
                                propietarios.append(nombre_completo)
                            
                        ids.append(str(equipo.id_equipo))
                        tipos.append(equipo.tipo)
                        marcas.append(equipo.marca)
                        modelos.append(equipo.modelo)
                        colores.append(equipo.color)
                        memorias.append(equipo.memoriaram)
                        procesadores.append(equipo.procesador)
                        sistemas.append(equipo.sistemaoperativo)
                        cargadores.append(equipo.modelocargador)
                        estados.append(equipo.estado)
                        
                        
                        contadorEquiposXHoja +=1
                        
                    
                #solo 9 empleados
                listaEquipos = zip(ids, tipos, marcas, modelos, colores, memorias, procesadores, sistemas, cargadores, estados, propietarios, urls_imagenes)
                
                contadorHojas = 3
                if contadorEquiposXHoja == 9:
                    high = 600 - ((contadorEquiposXHoja+1) * 33)
                else:
                    high = 600 - (contadorEquiposXHoja * 33)
                    
                        
            if contadorHojas == 1:
                contadorEquiposXHoja = 0
                for equipo in datosEquipos:
                    
                    contadorEquipos += 1 #10
                    if contadorEquipos <= 9:
                        imagen = equipo.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idempleado = equipo.id_empleado_id
                        if idempleado == None:
                            propietarios.append("Sin propietario")
                        else:
                            info_empleado = Empleados.objects.filter(id_empleado = idempleado)
                            
                            for dato in info_empleado:
                                nombre = dato.nombre
                                apellidos = dato.apellidos
                                nombre_completo = nombre + " " + apellidos
                                propietarios.append(nombre_completo)
                            
                        ids.append(str(equipo.id_equipo))
                        tipos.append(equipo.tipo)
                        marcas.append(equipo.marca)
                        modelos.append(equipo.modelo)
                        colores.append(equipo.color)
                        memorias.append(equipo.memoriaram)
                        procesadores.append(equipo.procesador)
                        sistemas.append(equipo.sistemaoperativo)
                        cargadores.append(equipo.modelocargador)
                        estados.append(equipo.estado)
                        
                        
                        contadorEquiposXHoja +=1
                        
                    
                #solo 9 empleados
                listaEquipos = zip(ids, tipos, marcas, modelos, colores, memorias, procesadores, sistemas, cargadores, estados, propietarios, urls_imagenes)
                
                contadorHojas = 2
                if contadorEquiposXHoja == 9:
                    high = 600 - ((contadorEquiposXHoja+1) * 33)
                else:
                    high = 600 - (contadorEquiposXHoja * 33)
                

            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            if activo == "A":
                c.drawString(380,750, "REPORTE EQUIPOS ACTIVOS")
            elif activo == "I":
                c.drawString(370,750, "REPORTE EQUIPOS INACTIVOS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            if activo == "A":
                c.drawString(180,660, 'Reporte Equipos Activos')
            elif activo == "I":
                c.drawString(180,660, 'Reporte Equipos Inactivos')
            
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_equipo = Paragraph('''ID''', styleBH)
            tipo = Paragraph('''Tipo''', styleBH)
            marca = Paragraph('''Marca''', styleBH)
            modelo = Paragraph('''Modelo''', styleBH)
            imagen = Paragraph('''Imagen.''', styleBH)
            ram = Paragraph('''RAM''', styleBH)
            procesador = Paragraph('''Procesador''', styleBH)
            sistemaop = Paragraph('''Sistema Operativo''', styleBH)
            carga = Paragraph('''Cargador''', styleBH)
            estado = Paragraph('''Estado''', styleBH)
            prop = Paragraph('''Propietario''', styleBH)
            filasTabla=[]
            filasTabla.append([id_equipo, tipo, marca, modelo, imagen, ram, procesador, sistemaop, carga, estado, prop])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
                
            cont = 0
            for id, tipo, marca, modelo, color, memoria, procesador, sistema, cargador, estado, propietario, imagenes in listaEquipos:
                campo_equipo = Paragraph(id, styleN)
                campo_tipo = Paragraph(tipo, styleN)
                campo_marca = Paragraph(marca, styleN)
                campo_modelo = Paragraph(modelo, styleN)
                campo_memoria = Paragraph(memoria, styleN)
                campo_procesador = Paragraph(procesador, styleN)
                campo_sistema = Paragraph(sistema, styleN)
                campo_cargador = Paragraph(cargador, styleN)
                campo_estado = Paragraph(estado, styleN)
                campo_propietario = Paragraph(propietario, styleN)
                
                fila = [campo_equipo, campo_tipo, campo_marca, campo_modelo, imagenes, campo_memoria, campo_procesador, campo_sistema, 
                        campo_cargador, campo_estado, campo_propietario]
                filasTabla.append(fila)
                
                high= high - 18 
                
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[.9 * cm, 1.5 * cm, 1.5 * cm, 2 * cm, 2 * cm, 1.5 * cm, 2.3 * cm, 2 * cm, 
                                                2 * cm,2 * cm,2.5 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            for fila in filasTabla:
                tabla.setStyle(([
                ('BACKGROUND', (0, 0), (10,0), colors.crimson),
                ('TEXTCOLOR',(0,0), (1, 1), colors.whitesmoke)
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
    
            #guardar pdf
            c.save()
            #obtener valores de bytesIO y esribirlos en la respuesta
            pdf = buffer.getvalue()
            buffer.close()
            respuesta.write(pdf)
            return respuesta
        
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def reporteImpresoras(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":

            activo= request.POST['activo']
        
        impresoras = Impresoras.objects.filter(activo__icontains = activo) #11 empleados
        
        numero_impresoras = 0
        for impresora in impresoras:
            numero_impresoras +=1
            
        if numero_impresoras == 0:
            numero_impresoras =1
        
        division = numero_impresoras // 9 #Resultado 1, sin residuo
        residuo = numero_impresoras%9 #residuo hay 2
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Impresoras'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        
        contadorHojas = 1
        for hoja2 in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            datosImpresoras= Impresoras.objects.filter(activo__icontains=activo) ##1 equipo
            
            
            ids =[]
            marcas = []
            modelos = []
            numseries = []
            tipos = []
            enredes = []
            ips = []
            estados = []
            areas = []
            urls_imagenes = []
            base_dir = str(settings.BASE_DIR)
            
            if contadorHojas == 3:
                contadorImpresorasXHoja = 0
                contadorImpresoras = 0
                for impresora in datosImpresoras:
                    
                    contadorImpresoras += 1 #10
                    if contadorImpresoras > 18 and contadorImpresoras <=27:
                        imagen = impresora.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                            
                        ids.append(str(impresora.id_impresora))
                        tipos.append(impresora.tipo)
                        marcas.append(impresora.marca)
                        modelos.append(impresora.modelo)
                        numseries.append(impresora.numserie)
                        if impresora.enred == "S":
                            enredes.append("SI")
                        elif impresora.enred == "N":
                            enredes.append("NO")
                        if impresora.ip == None:
                            ips.append("POR CABLE")
                        else:
                            ips.append(impresora.ip) 
                        estados.append(impresora.estado)
                        
                        idArea= impresora.id_area_id
                        
                        datosAreas= Areas.objects.filter(id_area=idArea)
                        for datos in datosAreas:
                            nombre = datos.nombre
                        areas.append(nombre)
                    
                        
                        
                        contadorImpresorasXHoja +=1
                        
                    
                #solo 9 empleados
                listaImpresoras = zip(ids, marcas, modelos, numseries, urls_imagenes, tipos, enredes, ips, estados, areas)
                
                contadorHojas = 4
                if contadorImpresorasXHoja == 9:
                    high = 600 - ((contadorImpresorasXHoja+1) * 33)
                else:
                    high = 600 - (contadorImpresorasXHoja * 33)
                    
                    
            
            if contadorHojas == 2:
                contadorImpresorasXHoja = 0
                contadorImpresoras = 0
                for impresora in datosImpresoras:
                    
                    contadorImpresoras += 1 #10
                    if contadorImpresoras > 9 and contadorImpresoras <=18:
                        imagen = impresora.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)

                        ids.append(str(impresora.id_impresora))
                        tipos.append(impresora.tipo)
                        marcas.append(impresora.marca)
                        modelos.append(impresora.modelo)
                        numseries.append(impresora.numserie)
                        if impresora.enred == "S":
                            enredes.append("SI")
                        elif impresora.enred == "N":
                            enredes.append("NO")
                        if impresora.ip == None:
                            ips.append("POR CABLE")
                        else:
                            ips.append(impresora.ip) 
                        estados.append(impresora.estado)
                        
                        idArea= impresora.id_area_id
                        
                        datosAreas= Areas.objects.filter(id_area=idArea)
                        for datos in datosAreas:
                            nombre = datos.nombre
                        areas.append(nombre)
 
                        contadorImpresorasXHoja +=1
                        
                    
                #solo 9 empleados
                listaImpresoras = zip(ids, marcas, modelos, numseries, urls_imagenes, tipos, enredes, ips, estados, areas)
                
                contadorHojas = 3
                if contadorImpresorasXHoja == 9:
                    high = 600 - ((contadorImpresorasXHoja+1) * 33)
                else:
                    high = 600 - (contadorImpresorasXHoja * 33)
                    
                        
            if contadorHojas == 1:
                contadorImpresorasXHoja = 0
                contadorImpresoras = 0
                for impresora in datosImpresoras:
                    
                    contadorImpresoras += 1 #10
                    if contadorImpresoras <= 9:
                        imagen = impresora.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                    
                            
                        ids.append(str(impresora.id_impresora))
                        tipos.append(impresora.tipo)
                        marcas.append(impresora.marca)
                        modelos.append(impresora.modelo)
                        numseries.append(impresora.numserie)
                        if impresora.enred == "S":
                            enredes.append("SI")
                        elif impresora.enred == "N":
                            enredes.append("NO")
                        if impresora.ip == None:
                            ips.append("POR CABLE")
                        else:
                            ips.append(impresora.ip) 
                        estados.append(impresora.estado)
                        
                        idArea= impresora.id_area_id
                        
                        datosAreas= Areas.objects.filter(id_area=idArea)
                        for datos in datosAreas:
                            nombre = datos.nombre
                        areas.append(nombre)
                    
                        
                        
                        contadorImpresorasXHoja +=1
                        
                    
                #solo 9 empleados
                listaImpresoras = zip(ids, marcas, modelos, numseries, urls_imagenes, tipos, enredes, ips, estados, areas)
                
                contadorHojas = 2
                if contadorImpresorasXHoja == 9:
                    high = 600 - ((contadorImpresorasXHoja+1) * 33)
                else:
                    high = 600 - (contadorImpresorasXHoja * 33)
                

            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            if activo == "A":
                c.drawString(360,750, "REPORTE IMPRESORAS ACTIVAS")
            elif activo == "I":
                c.drawString(350,750, "REPORTE IMPRESORAS INACTIVAS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            if activo == "A":
                c.drawString(150,660, 'Reporte Impresoras Activas')
            elif activo == "I":
                c.drawString(150,660, 'Reporte Impresoras Inactivas')

            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            idImpresora = Paragraph('''ID''', styleBH)
            marcaInfo = Paragraph('''Marca''', styleBH)
            modeloInfo = Paragraph('''Modelo''', styleBH)
            numserieInfo = Paragraph('''Num. Serie''', styleBH)
            imagenInfo = Paragraph('''Imagen.''', styleBH)
            tipoInfo= Paragraph('''Tipo''', styleBH)
            enredInfo = Paragraph('''Red''', styleBH)
            ipInfo = Paragraph('''Dirección IP''', styleBH)
            estadoInfo = Paragraph('''Estado''', styleBH)
            areaInfo = Paragraph('''Area''', styleBH)
            
            filasTabla=[]
            filasTabla.append([idImpresora,marcaInfo, modeloInfo, numserieInfo, imagenInfo, tipoInfo,enredInfo, ipInfo, estadoInfo, areaInfo  ])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
                
            cont = 0
            for id, marca, modelo, numserie, imagen, tipo, enred, ip, estado, area in listaImpresoras:
                campo_impresora = Paragraph(id, styleN)
                campo_marca = Paragraph(marca, styleN)
                campo_modelo = Paragraph(modelo, styleN)
                campo_numserie = Paragraph(numserie, styleN)
                campo_tipo = Paragraph(tipo, styleN)
                campo_enred = Paragraph(enred, styleN)
                campo_ip = Paragraph(ip, styleN)
                campo_estado = Paragraph(estado, styleN)
                campo_area = Paragraph(area, styleN)
                
                
                fila = [campo_impresora, campo_marca, campo_modelo,campo_numserie, imagen, campo_tipo, campo_enred, campo_ip,campo_estado, campo_area ]
                filasTabla.append(fila)
                
                high= high - 18 
                
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[.9 * cm, 1.5 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm, 1.5 * cm, 2.5 * cm, 
                                                2 * cm,2 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            for fila in filasTabla:
                tabla.setStyle(([
                ('BACKGROUND', (0, 0), (10,0), colors.crimson),
                ('TEXTCOLOR',(0,0), (1, 1), colors.whitesmoke)
            ]))
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 30, high)
            
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
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta
    
    else:
        return redirect('/login/') #redirecciona a url de inicio
       

def reporteRenovacionImp(request):
    
    if "idSesion" in request.session:
    
        renovacionImpresoras = Renovacion_Impresoras.objects.all()
        
        numero_impresoras = 0 #contador
        for impresora in renovacionImpresoras:
            numero_impresoras +=1 #20
            
        if numero_impresoras == 0:
            numero_impresoras =1
        
        division = numero_impresoras // 30 #Resultado 2, a fuerzas va a haber 2 hojas en el pdf
        residuo = numero_impresoras%30 #residuo hay 2
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 3
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Renovación Impresoras'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        
        contadorHojas = 1
        for hoja in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            renovacionImpresoras = Renovacion_Impresoras.objects.all()
            
            
            ids =[]
            modelos = []
            imagenes = []
            departamentos = []
            compras = []
            renovaciones = []
            base_dir = str(settings.BASE_DIR)
            
        
            if contadorHojas == 1:
                contadorImpresoras = 0
                contadorImpresorasxHoja = 0
                for datosRenovacion in renovacionImpresoras:
                        
                        
                    contadorImpresoras += 1 #10
                        
                        
                    if contadorImpresoras <= 9:
                        #Obtener solo empleados que quepan en la hoja
                        idImpresora= datosRenovacion.id_impresora_id
                        compra= datosRenovacion.fecha_compra
                        renovacion = datosRenovacion.fecha_renov
                        
                            
                        ids.append(idImpresora)
                        compras.append(compra)
                        renovaciones.append(renovacion)
                            
                        impresora = Impresoras.objects.filter(id_impresora=idImpresora)
                            
                        for datoImpresora in impresora:
                            marca = datoImpresora.marca
                            modelo = datoImpresora.modelo
                            datos_imp = "Impresora" + marca + "" + modelo 
                            modelos.append(datos_imp)
                            
                            area = datoImpresora.id_area_id
                            
                            datosArea = Areas.objects.filter(id_area = area)
                            
                            for dato in datosArea:
                                nombre = dato.nombre
                            
                            departamentos.append(nombre)
                            
                            imagen = datoImpresora.imagen
                            
                            urlimagen = base_dir + '/media/' + str(imagen)
                            img = Image(urlimagen,50,50)
                            imagenes.append(img)
                            
                        contadorImpresorasxHoja +=1
                    
                    #solo 9 empleados
                    listaImpresoras = zip(ids, modelos, imagenes, departamentos, compras, renovaciones)
                    contadorHojas = 2
                    if contadorImpresorasxHoja == 9:
                        high = 280 - ((contadorImpresorasxHoja+1) * 1)
                    else:
                        high = 280 - (contadorImpresorasxHoja * 1)
                
                

            
            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(340,750, "REPORTE RENOVACIÓN IMPRESORAS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            c.drawString(150,660, 'Reporte Renovación Impresoras')
            
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_renovacion = Paragraph('''ID''', styleBH)
            impresora_re = Paragraph('''Equipo''', styleBH)
            imagen_re = Paragraph('''Imagen''', styleBH)
            departamento_re = Paragraph('''Departamento''', styleBH)
            compra_re = Paragraph('''Fecha Compra.''', styleBH)
            renovacion_re = Paragraph('''Fecha Renovación''', styleBH)
            
            filasTabla=[]
            filasTabla.append([id_renovacion,impresora_re, imagen_re, departamento_re, compra_re, renovacion_re ])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
            for id_re, impresora, imagen, departamento, compra, renov in listaImpresoras:
                campo_id = Paragraph(str(id_re), styleN)
                campo_impresora = Paragraph(str(impresora), styleN)
                campo_departamento = Paragraph(str(departamento), styleN)
                campo_compra = Paragraph(str(compra), styleN)
                campo_renovacion = Paragraph(str(renov), styleN)
            
                
                fila = [campo_id, campo_impresora, imagen, campo_departamento, campo_compra, campo_renovacion]
                filasTabla.append(fila)
                
                high= high - 18 
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[1 * cm, 5 * cm, 4 * cm, 3 * cm, 3 * cm, 3 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))  
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 35, high)
            
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

        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta
    
    else:
        return redirect('/login/') #redirecciona a url de inicio


def reporteInsumosRequisicion(request):
    
    
    
    if "idSesion" in request.session:    
        
    
        insumos = Cartuchos.objects.filter(cantidad__in=[0,1], id_impresora__in =[1,2,3,5])
        
        numero_insumos = 0
        for insumo in insumos:
            numero_insumos +=1
            
        if numero_insumos == 0:
            numero_insumos =1
        
        division = numero_insumos // 9 #Resultado 1, sin residuo
        residuo = numero_insumos%9 #residuo hay 2
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Insumos Faltantes'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
    
        contadorHojas = 1
        for hoja2 in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            insumos= Cartuchos.objects.filter(cantidad__in=[0,1], id_impresora__in =[1,2,3,5]) #Dolo los insumos que tengan en su cantidad 1 o 0.
            
            
            ids =[]
            marcas = []
            modelos = []
            cantidades = []
            numseries = []
            colores = []
            urls_imagenes = []
            impresoras = []
            cantidades_compras = []
            base_dir = str(settings.BASE_DIR)
 
            if contadorHojas == 4:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 27 and contadorInsumos <= 36:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        if insumo.cantidad == 0:
                            compra_req = "2 cartuchos"
                        if insumo.cantidad == 1:
                            compra_req = "1 cartuchos"
                        cantidades_compras.append(compra_req)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                    
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras, cantidades_compras)
                
                contadorHojas = 5
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)        
            
            if contadorHojas == 3:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 18 and contadorInsumos <= 27:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        if insumo.cantidad == 0:
                            compra_req = "2 cartuchos"
                        if insumo.cantidad == 1:
                            compra_req = "1 cartuchos"
                        cantidades_compras.append(compra_req)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                        
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras, cantidades_compras)
                
                contadorHojas = 4
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
                    
            if contadorHojas == 2:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 9 and contadorInsumos <= 18:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        if insumo.cantidad == 0:
                            compra_req = "2 cartuchos"
                        if insumo.cantidad == 1:
                            compra_req = "1 cartuchos"
                        cantidades_compras.append(compra_req)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                    
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras,  cantidades_compras)
                
                contadorHojas = 3
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
                    
                        
            if contadorHojas == 1:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos <= 9:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        if idimpresora == 3:
                            if insumo.cantidad == 0:
                                compra_req = "3 cartuchos"
                            if insumo.cantidad == 1:
                                compra_req = "2 cartucho"
                        else:
                            if insumo.cantidad == 0:
                                compra_req = "2 cartuchos"
                            if insumo.cantidad == 1:
                                compra_req = "1 cartucho"

                        cantidades_compras.append(compra_req)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                        
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras, cantidades_compras)
                
                contadorHojas = 2
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
            
            base_dir = str(settings.BASE_DIR)
            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(400,750, "INSUMOS FALTANTES")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            c.drawString(200,660, 'Insumos Faltantes.')
 
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_insumo = Paragraph('''ID''', styleBH)
            marca = Paragraph('''Marca''', styleBH)
            modelo = Paragraph('''Modelo''', styleBH)
            cantidad= Paragraph('''Stock''', styleBH)
            nserie = Paragraph('''N° Serie''', styleBH)
            color = Paragraph('''Tinta''', styleBH)
            imagen = Paragraph('''Imagen.''', styleBH)
            impresora = Paragraph('''Impresora''', styleBH)
            cantidad_compra = Paragraph('''Cantidad Compra''', styleBH)
        
            filasTabla=[]
            filasTabla.append([id_insumo, marca, modelo, cantidad,nserie, color, imagen,impresora,cantidad_compra])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
                
            cont = 0
            for id, marca, modelo, cantidad,nserie,  color,  imagenes, impresora, cantidad_compra in listaInsumos:
                campo_insumo = Paragraph(str(id), styleN)
                campo_marca = Paragraph(marca, styleN)
                campo_modelo = Paragraph(modelo, styleN)
                campo_cantidad = Paragraph(str(cantidad), styleN)
                campo_nserie = Paragraph(nserie, styleN)
                campo_color = Paragraph(color, styleN)
                campo_impresora = Paragraph(impresora, styleN)
                campo_cantidadcompra = Paragraph(cantidad_compra, styleN)
                
                fila = [campo_insumo, campo_marca, campo_modelo, campo_cantidad,  campo_nserie, campo_color, imagenes, campo_impresora, campo_cantidadcompra]
                filasTabla.append(fila)
                
                high= high - 18 
                
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[.9 * cm, 1.5 * cm, 3* cm, 1.3 * cm, 2 * cm, 1.5 * cm, 2.3 * cm, 4 * cm, 3 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            contador = 0
            for fila in filasTabla:
                contador = contador + 1
                if contador == 1:
                    tabla.setStyle(([
                    ('BACKGROUND', (0, 0), (10,0), colors.crimson),
                    ('TEXTCOLOR',(0,0), (1, 1), colors.whitesmoke)
                    ]))
                
                if contador > 1:
                    tabla.setStyle(([
                    ('BACKGROUND', (8, 1), (10,contador), colors.lightcoral),
                    ]))
                
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 30, high)
            
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
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta

    else:
        return redirect('/login/') #redirecciona a url de inicio


def reporteInsumos(request):
    
    
    
    if "idSesion" in request.session:    
        
    
        insumos = Cartuchos.objects.all() #11 empleados
        
        numero_insumos = 0
        for insumo in insumos:
            numero_insumos +=1
            
        if numero_insumos == 0:
            numero_insumos =1
        
        division = numero_insumos // 9 #Resultado 1, sin residuo
        residuo = numero_insumos%9 #residuo hay 2
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Insumos'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
    
        contadorHojas = 1
        for hoja2 in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            insumos= Cartuchos.objects.all() ##1 equipo
            
            
            ids =[]
            marcas = []
            modelos = []
            cantidades = []
            numseries = []
            colores = []
            urls_imagenes = []
            impresoras = []
            base_dir = str(settings.BASE_DIR)
 
            if contadorHojas == 4:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 27 and contadorInsumos <= 36:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                    
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras)
                
                contadorHojas = 5
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)        
            
            if contadorHojas == 3:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 18 and contadorInsumos <= 27:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                        
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras)
                
                contadorHojas = 4
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
                    
            if contadorHojas == 2:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos > 9 and contadorInsumos <= 18:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                    
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras)
                
                contadorHojas = 3
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
                    
                        
            if contadorHojas == 1:
                contadorInsumos = 0
                contadorInsumosXHoja = 0
                for insumo in insumos:
                    
                    contadorInsumos += 1 #10
                    if contadorInsumos <= 9:
                        imagen = insumo.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idimpresora = insumo.id_impresora_id
                        
                        datosImpresora= Impresoras.objects.filter(id_impresora=idimpresora)
                        for dato in datosImpresora:
                            marca= dato.marca
                            modelo=dato.modelo
                        textoImpresora= marca + " " + modelo
                        impresoras.append(textoImpresora)
                        ids.append(insumo.id_cartucho)
                        marcas.append(insumo.marca)
                        modelos.append(insumo.modelo)
                        cantidades.append(insumo.cantidad)
                        numseries.append(insumo.nuserie)
                        colores.append(insumo.color)
                        
                        contadorInsumosXHoja +=1
                        
                    
                #solo 9 empleados
                listaInsumos = zip(ids, marcas, modelos, cantidades, numseries, colores, urls_imagenes, impresoras)
                
                contadorHojas = 2
                if contadorInsumosXHoja == 9:
                    high = 600 - ((contadorInsumosXHoja+1) * 33)
                else:
                    high = 600 - (contadorInsumosXHoja * 33)
            
            base_dir = str(settings.BASE_DIR)
            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(410,750, "REPORTE DE INSUMOS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            c.drawString(200,660, 'Reporte Insumos')
 
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_insumo = Paragraph('''ID''', styleBH)
            marca = Paragraph('''Marca''', styleBH)
            modelo = Paragraph('''Modelo''', styleBH)
            cantidad= Paragraph('''Cantidad''', styleBH)
            nserie = Paragraph('''N° Serie''', styleBH)
            color = Paragraph('''Color''', styleBH)
            imagen = Paragraph('''Imagen.''', styleBH)
            impresora = Paragraph('''Impresora''', styleBH)
        
            filasTabla=[]
            filasTabla.append([id_insumo, marca, modelo, cantidad,nserie, color, imagen,impresora])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
                
            cont = 0
            for id, marca, modelo, cantidad,nserie,  color,  imagenes, impresora in listaInsumos:
                campo_insumo = Paragraph(str(id), styleN)
                campo_marca = Paragraph(marca, styleN)
                campo_modelo = Paragraph(modelo, styleN)
                campo_cantidad = Paragraph(str(cantidad), styleN)
                campo_nserie = Paragraph(nserie, styleN)
                campo_color = Paragraph(color, styleN)
                campo_impresora = Paragraph(impresora, styleN)
                
                fila = [campo_insumo, campo_marca, campo_modelo, campo_cantidad,  campo_nserie, campo_color, imagenes, campo_impresora]
                filasTabla.append(fila)
                
                high= high - 18 
                
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[.9 * cm, 1.5 * cm, 4* cm, 2 * cm, 2 * cm, 1.5 * cm, 2.3 * cm, 4 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            for fila in filasTabla:
                tabla.setStyle(([
                ('BACKGROUND', (0, 0), (10,0), colors.crimson),
                ('TEXTCOLOR',(0,0), (1, 1), colors.whitesmoke)
            ]))
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 50, high)
            
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
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta

    else:
        return redirect('/login/') #redirecciona a url de inicio


def pdfInfoEquipo(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":
        
            equipo_recibido= request.POST['idequipo']
            
        datosEquipo = Equipos.objects.filter(id_equipo = equipo_recibido)
        
        for dato in datosEquipo:
            propietario = dato.id_empleado_id
            
            if propietario == None:
                nombreProp = "Sin propietario"
            else:
                datosPropietario = Empleados.objects.filter(id_empleado = propietario)
                
                for datoPropietario in datosPropietario:
                    nombre = datoPropietario.nombre
                    apellidos = datoPropietario.apellidos
                nombreProp = nombre + " " + apellidos
                
        datosRenovacion = Renovacion_Equipos.objects.filter(id_equipo = equipo_recibido)
        
        for dato in datosRenovacion:
            compra = dato.fecha_compra
            renovacion = dato.fecha_renov  
            
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", 
                    "Octubre", "Noviembre", "Diciembre"]
            
            contadorMeses = 0
            mesCompra = compra.strftime('%m')
            intmesCompra = int(mesCompra)
            
            messtr = ""
            for mes in meses:
                contadorMeses += 1
                if contadorMeses == intmesCompra:
                    messtr = mes
            
            
            
            solo_compra_str = compra.strftime('%d de '+ messtr+ ' de %Y')
            solo_renovacion_str = renovacion.strftime('%d de '+ messtr+ ' de %Y')
        
        
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Info Equipo'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR)
        #nombre de empresa
        
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
        
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400,750, "INFORMACIÓN DE EQUIPO")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
        
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
        c.drawString(200,660, 'Información de Equipo')
        

        for dato in datosEquipo:
            c.setFont('Helvetica-Bold', 24)
            c.drawString(200,610, 'Número de equipo: '+str(dato.id_equipo))
            
            c.setFont('Helvetica-Bold', 26)
            c.drawString(80,580, dato.tipo + " " + dato.marca + " " + dato.modelo)
            
            imagen = str(dato.imagen)  
            
            imagenCompleta = base_dir+"/media/"+imagen 
            c.drawImage(imagenCompleta, 210,430,width=160,height=140)
            
            if nombreProp == "Sin propietario":
                c.setFont('Helvetica-Bold', 20)
                c.drawString(190,390, "Propietario: " + nombreProp)
            else:
                c.setFont('Helvetica-Bold', 20)
                c.drawString(90,390, "Propietario: " + nombreProp)
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(70,360, "Fecha de Compra")
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(330,360, "Fecha de Renovación")
            
            carrito = base_dir+'/static/images/capng.png'   
            c.drawImage(carrito, 110,285,100,70, preserveAspectRatio=True)
            
            carritocompra = base_dir+'/static/images/cacompng.png'   
            c.drawImage(carritocompra, 390,285,100,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 18)
            c.drawString(60,270, str(solo_compra_str))
            
            c.setFont('Helvetica-Bold', 18)
            c.drawString(340,270, str(solo_renovacion_str))
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(60,230, "Características")
            
            tabla_id = dato.id_equipo
            tabla_tipo = dato.tipo
            tabla_marca = dato.marca
            tabla_modelo = dato.modelo
            tabla_ram = dato.memoriaram
            tabla_procesador = dato.procesador
            tabla_sistema = dato.sistemaoperativo
            tabla_cargador = dato.modelocargador
            tabla_estado = dato.estado
        
        
        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        id_equipo = Paragraph('''ID''', styleBH)
        tipo = Paragraph('''Tipo''', styleBH)
        marca = Paragraph('''Marca''', styleBH)
        modelo = Paragraph('''Modelo''', styleBH)
        ram = Paragraph('''RAM''', styleBH)
        procesador = Paragraph('''Procesador''', styleBH)
        sistemaop = Paragraph('''Sistema Operativo''', styleBH)
        carga = Paragraph('''Cargador''', styleBH)
        estado = Paragraph('''Estado''', styleBH)
        filasTabla=[]
        filasTabla.append([id_equipo, tipo, marca, modelo, ram, procesador, sistemaop, carga, estado])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 170
        campo_equipo = Paragraph(str(tabla_id), styleN)
        campo_tipo = Paragraph(tabla_tipo, styleN)
        campo_marca = Paragraph(tabla_marca, styleN)
        campo_modelo = Paragraph(tabla_modelo, styleN)
        campo_memoria = Paragraph(tabla_ram, styleN)
        campo_procesador = Paragraph(tabla_procesador, styleN)
        campo_sistema = Paragraph(tabla_sistema, styleN)
        campo_cargador = Paragraph(tabla_cargador, styleN)
        campo_estado = Paragraph(tabla_estado, styleN)
                
        fila = [campo_equipo, campo_tipo, campo_marca, campo_modelo, campo_memoria, campo_procesador, campo_sistema, 
                        campo_cargador, campo_estado]
        filasTabla.append(fila)
                
        high= high - 18  
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[1 * cm, 2 * cm, 2 * cm, 2 * cm, 2* cm, 4 * cm, 2 * cm, 2 * cm, 2 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 40, high)
        
        #Tabla de periféricos
        filasTablaPerifericos = []
        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        cabeceraMouse = Paragraph('''Mouse''', styleBH)
        cabeceraTeclado = Paragraph('''Teclado''', styleBH)
        cabeceraMonitor = Paragraph('''Monitor''', styleBH)
        filasTablaPerifericos.append([cabeceraMouse, cabeceraTeclado, cabeceraMonitor])
        
        #Sacar información de Mouse, teclado y monitor.
        mouseCompleto = ""
        tecladoCompleto = ""
        monitorCompleto = ""
        
        #Mouse
        datosMouse = Mouses.objects.filter(id_equipo_id__id_equipo = equipo_recibido)
        if datosMouse:
            for datoMouse in datosMouse:
                tipoConexión=""
                conexionMouse = datoMouse.conexion
                if conexionMouse == "A":
                    tipoConexion = "alámbrica"
                elif conexionMouse == "I":
                    tipoConexion = "inalámbrica"
                marcaMouse = datoMouse.marca
                modeloMouse = datoMouse.modelo
            mouseCompleto = "Mouse "+ marcaMouse + " modelo "+ modeloMouse + ", conexión " + tipoConexion
        else:
            mouseCompleto = "No cuenta con mouse."
        
        #Teclado
        datosTeclado = Teclados.objects.filter(id_equipo_id__id_equipo = equipo_recibido)
        if datosTeclado:
            for datoTeclado in datosTeclado:
                tipoConexionTeclado = ""
                conexionTeclado = datoTeclado.conexion
                if conexionTeclado == "A":
                    tipoConexionTeclado = "alámbrica"
                elif conexionTeclado == "I":
                    tipoConexionTeclado = "inalámbrica"
                marcaTeclado = datoTeclado.marca
                modeloTeclado = datoTeclado.model
            tecladoCompleto = "Teclado "+marcaTeclado + " modelo "+modeloTeclado + ", conexión "+tipoConexionTeclado
        
        else:
            tecladoCompleto = "No cuenta con teclado."
        
        #Monitor
        datosMonitor = Monitores.objects.filter(id_equipo_id__id_equipo = equipo_recibido)
        if datosMonitor:
            for datoMonitor in datosMonitor:
                marcaMonitor = datoMonitor.marca
                modeloMonitor = datoMonitor.modelo
            monitorCompleto = "Monitor "+marcaMonitor + " modelo "+modeloMonitor
        else:
            monitorCompleto = "No cuenta con monitor."
        
        
        
        mouseTabla = Paragraph(mouseCompleto, styleN)
        tecladoTabla = Paragraph(tecladoCompleto, styleN)
        monitorTabla = Paragraph(monitorCompleto, styleN)
        filasTablaPerifericos.append([mouseTabla, tecladoTabla, monitorTabla])
        
        
        tabla2 = Table(filasTablaPerifericos, colWidths=[5*cm,5*cm,5*cm])
        tabla2.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        tabla2.wrapOn(c, width, height)
        tabla2.drawOn(c, 100, 90)
        
        
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
        
        
        #SEGUNDA HOJA ----------------------------------------------------------------------------------------
        
        mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo__icontains=tabla_id) #11 empleados
        
        numero_mantanimientos = 0
        for mant in mantenimientos:
            numero_mantanimientos +=1
            
        if numero_mantanimientos == 0:
            numero_mantanimientos =1
        
        division = numero_mantanimientos // 9 #Resultado 1, sin residuo
        residuo = numero_mantanimientos%9 #residuo hay 2
        
        
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        contadorHojas = 1
        mantenimientos = CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo__icontains=tabla_id)
                
        id_mantenimientos = []
        operaciones = []
        fechas = []
        observaciones = []
        for hoja in range(division):
            
            if contadorHojas == 4:
                contadorMantenimientos = 0
                contadorMantenimientosxHoja = 0
            
                for mantenimiento in mantenimientos:
                    
                    contadorMantenimientos += 1
                    
                    if contadorMantenimientos > 30 and contadorMantenimientos <= 40:
                        id = mantenimiento.id_calmantenimiento
                        operacion = mantenimiento.operacion
                        fecha = mantenimiento.fecha
                        observacion = mantenimiento.observaciones
                        
                        id_mantenimientos.append(str(id))
                        operaciones.append(operacion)
                        fechas.append(fecha)
                        observaciones.append(observacion)
                        
                        contadorMantenimientosxHoja+=1
                
                listaMantenimientos = zip(id_mantenimientos, operaciones, fechas, observaciones)
                
                contadorHojas = 5
                if contadorMantenimientosxHoja == 20:
                    high = 600 - ((contadorMantenimientosxHoja+1) * 33)
                else:
                    high = 600 - (contadorMantenimientosxHoja * 33)
            
            if contadorHojas == 3:
                contadorMantenimientos = 0
                contadorMantenimientosxHoja = 0
            
                for mantenimiento in mantenimientos:
                    
                    contadorMantenimientos += 1
                    
                    if contadorMantenimientos > 20 and contadorMantenimientos <= 30:
                        id = mantenimiento.id_calmantenimiento
                        operacion = mantenimiento.operacion
                        fecha = mantenimiento.fecha
                        observacion = mantenimiento.observaciones
                        
                        id_mantenimientos.append(str(id))
                        operaciones.append(operacion)
                        fechas.append(fecha)
                        observaciones.append(observacion)
                        
                        contadorMantenimientosxHoja+=1
                
                listaMantenimientos = zip(id_mantenimientos, operaciones, fechas, observaciones)
                
                contadorHojas = 4
                if contadorMantenimientosxHoja == 20:
                    high = 600 - ((contadorMantenimientosxHoja+1) * 33)
                else:
                    high = 600 - (contadorMantenimientosxHoja * 33)
                    
            
            if contadorHojas == 2:
                contadorMantenimientos = 0
                contadorMantenimientosxHoja = 0
            
                for mantenimiento in mantenimientos:
                    
                    contadorMantenimientos += 1
                    
                    if contadorMantenimientos > 10 and contadorMantenimientos <= 20:
                        id = mantenimiento.id_calmantenimiento
                        operacion = mantenimiento.operacion
                        fecha = mantenimiento.fecha
                        observacion = mantenimiento.observaciones
                        
                        id_mantenimientos.append(str(id))
                        operaciones.append(operacion)
                        fechas.append(fecha)
                        observaciones.append(observacion)
                        
                        contadorMantenimientosxHoja+=1
                
                listaMantenimientos = zip(id_mantenimientos, operaciones, fechas, observaciones)
                
                contadorHojas = 3
                if contadorMantenimientosxHoja == 20:
                    high = 600 - ((contadorMantenimientosxHoja+1) * 33)
                else:
                    high = 600 - (contadorMantenimientosxHoja * 33)
                    
            
            if contadorHojas == 1:
                contadorMantenimientos = 0
                contadorMantenimientosxHoja = 0
            
                for mantenimiento in mantenimientos:
                    
                    contadorMantenimientos += 1
                    
                    if contadorMantenimientos <= 10:
                        id = mantenimiento.id_calmantenimiento
                        operacion = mantenimiento.operacion
                        fecha = mantenimiento.fecha
                        observacion = mantenimiento.observaciones
                        
                        id_mantenimientos.append(str(id))
                        operaciones.append(operacion)
                        fechas.append(fecha)
                        observaciones.append(observacion)
                        
                        contadorMantenimientosxHoja+=1
                
                listaMantenimientos = zip(id_mantenimientos, operaciones, fechas, observaciones)
                
                contadorHojas = 2
                if contadorMantenimientosxHoja == 20:
                    high = 630 - ((contadorMantenimientosxHoja+1) * 33)
                else:
                    high = 630 - (contadorMantenimientosxHoja * 33)
                
            #Lleno el arreglo de mantenimientos
            
            base_dir = str(settings.BASE_DIR)
            #nombre de empresa
            
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(400,750, "INFORMACIÓN DE EQUIPO")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            c.drawString(180,660, 'Mantenimientos de Equipo')
            
            
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10
            
            
            id_operacion = Paragraph('''Id Operación''', styleBH)
            operacion = Paragraph('''Operación''', styleBH)
            fecha = Paragraph('''Fecha''', styleBH)
            observaciones = Paragraph('''Observaciones''', styleBH)
            filasTabla=[]
            filasTabla.append([id_operacion, operacion, fecha, observaciones])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
            for id, operacion, fecha, observacion in listaMantenimientos:
                campo_mant = Paragraph(str(id), styleN)
                campo_operacion = Paragraph(operacion, styleN)
                campo_fecha = Paragraph(str(fecha), styleN)
                campo_observacion = Paragraph(observacion, styleN)
                
                fila = [campo_mant, campo_operacion, campo_fecha, campo_observacion]
                filasTabla.append(fila)
                
                high= high - 18 
                    
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[3 * cm, 4 * cm, 4 * cm, 8 * cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 40, high)
            
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

    else:
        return redirect('/login/') #redirecciona a url de inicio


def pdfInfoImpresora(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":
        
            impresora_recibido= request.POST['idimpresora']
            
        datosImpresora = Impresoras.objects.filter(id_impresora = impresora_recibido)
        
        for dato in datosImpresora:
            departamento = dato.id_area_id
            
            if departamento == None:
                nombre = "Sin departamento"
            else:
                datosDepartamento = Areas.objects.filter(id_area = departamento)
                
                for datoDepartamento in datosDepartamento:
                    nombre = datoDepartamento.nombre
                    color = datoDepartamento.color
                
                
        datosRenovacion = Renovacion_Impresoras.objects.filter(id_impresora = impresora_recibido)
        
        for dato in datosRenovacion:
            compra = dato.fecha_compra
            renovacion = dato.fecha_renov  
            
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", 
                    "Octubre", "Noviembre", "Diciembre"]
            
            contadorMeses = 0
            mesCompra = compra.strftime('%m')
            intmesCompra = int(mesCompra)
            
            messtr = ""
            for mes in meses:
                contadorMeses += 1
                if contadorMeses == intmesCompra:
                    messtr = mes
            
            
            
            solo_compra_str = compra.strftime('%d de '+ messtr+ ' de %Y')
            solo_renovacion_str = renovacion.strftime('%d de '+ messtr+ ' de %Y')
        
        
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Impresoras General'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR)
        #nombre de empresa
        
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
        
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
        
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400,750, "INFORMACIÓN DE IMPRESORA")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
        
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
        c.drawString(200,660, 'Información de Impresora')
        
 
        for dato in datosImpresora:
            c.setFont('Helvetica-Bold', 24)
            c.drawString(200,610, 'Número de impresora: '+ str(dato.id_impresora))
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(70,580, dato.marca + " " + dato.modelo + " " + dato.tipo)
            
            imagen = str(dato.imagen)  
            
            imagenCompleta = base_dir+"/media/"+imagen 
            c.drawImage(imagenCompleta, 240,420,width=150,height=150)
            
            if nombre == "Sin departamento":
                c.setFont('Helvetica-Bold', 20)
                c.drawString(190,370, "Departamento: " + nombre)
            else:
                c.setFont('Helvetica-Bold', 20)
                c.drawString(120,390, "Departamento: " + nombre)
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(70,360, "Fecha de Compra")
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(330,360, "Fecha de Renovación")
            
            carrito = base_dir+'/static/images/capng.png'   
            c.drawImage(carrito, 110,285,100,70, preserveAspectRatio=True)
            
            carritocompra = base_dir+'/static/images/cacompng.png'   
            c.drawImage(carritocompra, 390,285,100,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 18)
            c.drawString(60,270, str(solo_compra_str))
            
            c.setFont('Helvetica-Bold', 18)
            c.drawString(340,270, str(solo_renovacion_str))
            
            c.setFont('Helvetica-Bold', 22)
            c.drawString(60,230, "Características")
            
            tabla_id = dato.id_impresora
            tabla_marca = dato.marca
            tabla_modelo = dato.modelo
            tabla_tipo = dato.tipo
            tabla_enred= dato.enred
            tabla_ip = dato.ip
            tabla_estado = dato.estado
            tabla_activo = dato.activo
        
        
        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        id_impresora = Paragraph('''ID''', styleBH)
        marca = Paragraph('''Marca''', styleBH)
        modelo = Paragraph('''Modelo''', styleBH)
        tipo = Paragraph('''Tipo''', styleBH)
        red = Paragraph('''En red''', styleBH)
        ip = Paragraph('''Dirección IP''', styleBH)
        estado = Paragraph('''Estado''', styleBH)
        activo = Paragraph('''Activo''', styleBH)
        
        filasTabla=[]
        filasTabla.append([id_impresora, marca, modelo,  tipo, red, ip, estado, activo ])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 170
        campo_impresora = Paragraph(str(tabla_id), styleN)
        campo_marca = Paragraph(tabla_marca, styleN)
        campo_modelo = Paragraph(tabla_modelo, styleN)
        campo_tipo = Paragraph(tabla_tipo, styleN)
        campo_red = Paragraph(tabla_enred, styleN)
        campo_ip = Paragraph(tabla_ip, styleN)
        campo_estado = Paragraph(tabla_estado, styleN)
        campo_activo = Paragraph(tabla_activo, styleN)
        
                
        fila = [campo_impresora, campo_marca, campo_modelo,  campo_tipo, campo_red, campo_ip, campo_estado, 
                        campo_activo]
        filasTabla.append(fila)
                
        high= high - 18  
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[1 * cm, 2 * cm, 2.5 * cm, 2 * cm, 2* cm, 4 * cm, 2 * cm, 2 * cm, 2 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 60, high)
        
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
        
        
        #SEGUNDA HOJA ----------------------------------------------------------------------------------------
        
        cartuchos= Cartuchos.objects.filter(id_impresora_id__id_impresora__icontains=tabla_id) #11 empleados
        
        numero_cartuchos = 0
        for cart in cartuchos:
            numero_cartuchos +=1
            
        if numero_cartuchos == 0:
            numero_cartuchos =1
        
        division = numero_cartuchos // 9 #Resultado 1, sin residuo
        residuo = numero_cartuchos%9 #residuo hay 2
        
        
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        contadorHojas = 1
        cartuchos = Cartuchos.objects.filter(id_impresora_id__id_impresora__icontains=tabla_id)
                
        id_cartuchos = []
        marcas = []
        modelos = []
        urls_imagenes = []
        colores = []
        series  = []
        cantidades = []
        for hoja in range(division):
            
            if contadorHojas == 1:
                contadorCartuchos = 0
                contadorCartuchosxHoja = 0
            
                for cartucho in cartuchos:
                    
                    contadorCartuchos += 1
                    
                    if contadorCartuchos <=10:
                        id = cartucho.id_cartucho
                        marca = cartucho.marca
                        modelo = cartucho.modelo
                        imagen = cartucho.imagenCartucho
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,50,50)
                        urls_imagenes.append(img)
                        color= cartucho.color
                        serie=cartucho.nuserie
                        cantidad=cartucho.cantidad
                        
                        
                        id_cartuchos.append(str(id))
                        marcas.append(marca)
                        modelos.append(modelo)
                        colores.append(color)
                        series.append(serie)
                        cantidades.append(cantidad)
                        
                        contadorCartuchosxHoja+=1
                
                listaCartuchos = zip(id_cartuchos, marcas, modelos, urls_imagenes, colores, series, cantidades )
                
            
                
                contadorHojas = 2
                if contadorCartuchosxHoja == 20:
                    high = 600 - ((contadorCartuchosxHoja+1) * 33)
                else:
                    high = 600 - (contadorCartuchosxHoja * 33)
                
            #Lleno el arreglo de mantenimientos
            
            base_dir = str(settings.BASE_DIR)
            #nombre de empresa
            
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            c.drawString(400,750, "INFORMACIÓN DE CARTUCHO")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            c.drawString(180,660, 'Cartuchos de Impresora')
            
            
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10
            
            
            id_cartucho = Paragraph('''Id Cartucho''', styleBH)
            marca = Paragraph('''Marca''', styleBH)
            modelo = Paragraph('''Modelo''', styleBH)
            imagen = Paragraph('''Imagen.''', styleBH)
            color = Paragraph('''Color''', styleBH)
            serie = Paragraph('''Num. Serie''', styleBH)
            cantidad = Paragraph('''Cantidad''', styleBH)
            filasTabla=[]
            filasTabla.append([id_cartucho, marca, modelo, imagen, color, serie, cantidad])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
            for id, marcas, modelos, imagenes,colores,series,cantidades in listaCartuchos:
                campo_cart = Paragraph(str(id), styleN)
                campo_marca = Paragraph(marcas, styleN)
                campo_modelo = Paragraph(str(modelos), styleN)
                
                campo_color = Paragraph(colores, styleN)
                campo_serie = Paragraph(series, styleN)
                campo_cantidad = Paragraph(str(cantidades), styleN)
            
                
                fila = [campo_cart, campo_marca, campo_modelo,imagenes ,campo_color, campo_serie, campo_cantidad ]
                filasTabla.append(fila)
                
                high= high - 18 
                    
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[2 * cm, 2* cm, 3 * cm, 4 * cm, 2*cm, 3.5*cm, 2*cm])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 40, high)
            
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
    
    else:
        return redirect('/login/') #redirecciona a url de inicio

def qrEquipo(request):
    
    id_admin=request.session["idSesion"]
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
        
    cartuchosNoti = notificacionInsumos()
    mantenimientosNoti = notificacionLimpiezas()
    numeroNoti = numNoti()
        
    foto = fotoAdmin(request)
    
    if "idSesion" in request.session:
        
        return render(request, "Equipos/qrEquipo.html", {"nombreCompleto": nombreCompleto, "correo": correo, "cartuchosNoti": cartuchosNoti, "mantenimientosNoti":mantenimientosNoti,"numeroNoti":numeroNoti,"foto":foto } )
    else:
        return redirect('/login/') #redirecciona a url de inicio

def qrImpresora(request):
    
    id_admin=request.session["idSesion"]
    nombre = request.session['nombres']
    apellidos = request.session['apellidos']
    correo = request.session['correoSesion']
    nombreCompleto = nombre + " " + apellidos
        
    cartuchosNoti = notificacionInsumos()
    mantenimientosNoti = notificacionLimpiezas()
    numeroNoti = numNoti()
        
    foto = fotoAdmin(request)
    if "idSesion" in request.session:
        return render(request, "Impresoras/qrImpresora.html", {"nombreCompleto": nombreCompleto, "correo": correo, "cartuchosNoti": cartuchosNoti, "mantenimientosNoti":mantenimientosNoti,"numeroNoti":numeroNoti,"foto":foto })
    
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
    
#EXCEEELES

def xlDepartamentos(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Departamentos'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Departamentos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Departamento','Nombre', 'Color', 'Número de empleados']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    cantidad_empleados = []
    infoAreas = Areas.objects.all()
        
    for area in infoAreas:
        id_area_una = area.id_area
        areaInt = int(id_area_una)
            
        empleadosEnArea = Empleados.objects.filter(id_area_id__id_area = areaInt)#filtro de los empleados que esten dentro de un area especifica
            
        numero_empleados = 0
        for empleado in empleadosEnArea:
            numero_empleados+=1
            
        cantidad_empleados.append(str(numero_empleados)+" empleados")
    
    #lista la lista de cantidad_empleados
        
    areas = Areas.objects.all()
    
    datosAreas = []
    cont=0
    color = ""
    for x in areas:
        cont+=1
        if x.color == "label bg-red":
            color = "Rojo"
        elif x.color == "label bg-pink":
            color = "Rosa"
        elif x.color == "label bg-purple":
            color = "Morado"
        elif x.color == "label bg-indigo":
            color = "Indigo"
        elif x.color == "label bg-blue":
            color = "Azul"
        elif x.color == "label bg-cyan":
            color = "Cyan"
        elif x.color == "label bg-teal":
            color = "Teal"
        elif x.color == "label bg-Green":
            color = "Verde"
        elif x.color == "label bg-Light-Green":
            color = "Verde bajo"
        elif x.color == "label bg-lime":
            color = "Lima"
        elif x.color == "label bg-yellow":
            color = "Amarillo"
        elif x.color == "label bg-amber":
            color = "Amber"
        elif x.color == "label bg-orange":
            color = "Naranja"
        elif x.color == "label bg-deep-orange":
            color = "Naranja Oscuro"
        elif x.color == "label bg-brown":
            color = "Cafe"
        elif x.color == "label bg-grey":
            color = "Gris"
        elif x.color == "label bg-blue-grey":
            color = "Gris azulado"
        elif x.color == "label bg-black":
            color = "Negro"
            
        datosAreas.append([x.id_area, x.nombre, color, cantidad_empleados[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for area in datosAreas:
        numero_fila+=1
        for columna in range(len(area)):
            hoja.write(numero_fila, columna, str(area[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    



def xlEmpleados(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Empleados'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Empleados')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Nombre', 'Apellidos', 'Departamento', 'Puesto', 'Correo']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    departamentos = []
    infoEmpleados = Empleados.objects.filter(activo = activoa)
        
    for empleado in infoEmpleados:
        id_depa = empleado.id_area_id
            
        datosArea = Areas.objects.filter(id_area = id_depa)#filtro de los empleados que esten dentro de un area especifica
        
        for dato in datosArea:
            nombre = dato.nombre
        
        departamentos.append(nombre)
    
    #lista la lista de departamentos de empleados
        
    empleados = Empleados.objects.filter(activo = activoa)
    
    datosEmpleados = []
    cont=0
    for x in empleados:
        cont+=1
        datosEmpleados.append([x.id_empleado, x.nombre, x.apellidos, departamentos[cont-1], 
                               x.puesto, x.correo])
            
        
    estilo_fuente = xlwt.XFStyle()
    for empleadito in datosEmpleados:
        numero_fila+=1
        for columna in range(len(empleadito)):
            hoja.write(numero_fila, columna, str(empleadito[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    
    #creación 
    
def xlEquipos(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Equipos'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Tipo', 'Marca', 'Modelo', 'Color', 'RAM', 'Procesador', 'SO', 'Cargador', 'Propietario', 'Departamento', 'Estado']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    propietarios = []
    departamentos = []
    cargadores = []
    infoEquipos = Equipos.objects.filter(activo = activoa)
        
    for equipo in infoEquipos:
        id_emp = equipo.id_empleado_id
        mcargador = equipo.modelocargador
        
        if id_emp == None and mcargador == "":
            nombreEmpleado = "Sin propietario"
            departamento = "Sin departamento"
            cargador = "Sin cargador"
            
            propietarios.append(nombreEmpleado)
            departamentos.append(departamento)
            cargadores.append(cargador)
        
        elif id_emp == None:
            nombreEmpleado = "Sin propietario"
            departamento = "Sin departamento"
            cargador = equipo.modelocargador
            
            propietarios.append(nombreEmpleado)
            departamentos.append(departamento)
            cargadores.append(cargador)
        
        elif mcargador == "":
            cargador = "Sin cargador"
            datosEmpleado = Empleados.objects.filter(id_empleado = id_emp)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEmpleado:
                nombre = dato.nombre
                apellidos = dato.apellidos
                id_depa = dato.id_area_id
                
                infoDepa = Areas.objects.filter(id_area = id_depa)
                for dato in infoDepa:
                    departamento = dato.nombre
            nombreEmpleado = nombre + " " + apellidos
            
            propietarios.append(nombreEmpleado)
            departamentos.append(departamento)
            cargadores.append(cargador)
            
        else:
            datosEmpleado = Empleados.objects.filter(id_empleado = id_emp)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEmpleado:
                nombre = dato.nombre
                apellidos = dato.apellidos
                id_depa = dato.id_area_id
                
                infoDepa = Areas.objects.filter(id_area = id_depa)
                for dato in infoDepa:
                    departamento = dato.nombre
            nombreEmpleado = nombre + " " + apellidos
            cargador = equipo.modelocargador
            
            propietarios.append(nombreEmpleado)
            departamentos.append(departamento)
            cargadores.append(cargador)
        
        
    
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    equipos = Equipos.objects.filter(activo = activoa)
    
    datosEquipos = []
    cont=0
    for x in equipos:
        cont+=1
        datosEquipos.append([x.id_equipo, x.tipo, x.marca, x.modelo, x.color, x.memoriaram, x.procesador, 
                             x.sistemaoperativo, cargadores[cont-1], propietarios[cont-1], departamentos[cont-1], 
                             x.estado])
            
        
    estilo_fuente = xlwt.XFStyle()
    for equipito in datosEquipos:
        numero_fila+=1
        for columna in range(len(equipito)):
            hoja.write(numero_fila, columna, str(equipito[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 
    
def xlRenovacionEquipos(request):
            
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Renovación Equipos'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Renovacion Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Equipo', 'Propietario', 'Departamento', 'Fecha de compra', 'Fecha de renovación']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    listaEquipos = []
    listaPropietarios =[]
    listaDepartamentos = []
    infoRenovaciones = Renovacion_Equipos.objects.all()
        
    for renovacion in infoRenovaciones:
        id_equipo_renov = renovacion.id_equipo_id
        
        infoEquipo = Equipos.objects.filter(id_equipo = id_equipo_renov)
        
        for dato in infoEquipo:
            tipo = dato.tipo
            marca = dato.marca
            modelo = dato.modelo
            color = dato.color
            propietario = dato.id_empleado_id
            
            if propietario == None:
                propietarioEq = "Sin propietario"
                departamento = "Sin departamento"
            else:
                datosPropietario = Empleados.objects.filter(id_empleado = propietario)
                
                for d in datosPropietario:
                    nombre = d.nombre
                    apellidos = d.apellidos
                    id_area_prop = d.id_area_id
                    
                    infoArea = Areas.objects.filter(id_area = id_area_prop)
                    for datoArea in infoArea:
                        departamento = datoArea.nombre
                    
                propietarioEq = nombre + " " + apellidos
            
        equipoCompleto = tipo + " " + marca + " " + modelo + " " + color
        listaEquipos.append(equipoCompleto)
        listaPropietarios.append(propietarioEq)
        listaDepartamentos.append(departamento)
        
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    renovaciones = Renovacion_Equipos.objects.all()
    
    datosRenovaviones = []
    cont=0
    for x in renovaciones:
        cont+=1
        datosRenovaviones.append([x.id_equipo_id, listaEquipos[cont-1], listaPropietarios[cont-1], listaDepartamentos[cont-1], 
                             x.fecha_compra, x.fecha_renov])
            
        
    estilo_fuente = xlwt.XFStyle()
    for renovacionsita in datosRenovaviones:
        numero_fila+=1
        for columna in range(len(renovacionsita)):
            hoja.write(numero_fila, columna, str(renovacionsita[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    
    #creación 
    
    
def xlImpresoras(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Impresoras'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Impresoras')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Marca', 'Modelo', 'N° Serie', 'Tipo', 'En red', 'Dirección IP', 'Estado', 'Área']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    enRed = []
    direccionesIP = []
    areas = []
    infoImpresoras = Impresoras.objects.filter(activo = activoa)
        
    for impresora in infoImpresoras:
        enredd = impresora.enred
        areaImpresora = impresora.id_area_id
        
        
        if enredd == "N":
            red = "No"
            direccionIP = "-"
        else:
            red = "Si"
            direccionIP = impresora.ip
            
        infoArea = Areas.objects.filter(id_area = areaImpresora)
        for dato in infoArea:
            nombreArea = dato.nombre

        enRed.append(red)
        direccionesIP.append(direccionIP)
        areas.append(nombreArea)
        
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    impresoras = Impresoras.objects.filter(activo = activoa)
    
    datosImpresoras = []
    cont=0
    for x in impresoras:
        cont+=1
        datosImpresoras.append([x.id_impresora, x.marca, x.modelo, x.numserie, x.tipo, 
                                enRed[cont-1], direccionesIP[cont-1], x.estado, 
                             areas[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for impresorita in datosImpresoras:
        numero_fila+=1
        for columna in range(len(impresorita)):
            hoja.write(numero_fila, columna, str(impresorita[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 
    
    
def xlRenovacionImpresoras(request):
            
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Renovación Impresoras'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Renovacion Impresoras')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Impresora','Modelo', 'Departamento', 'Fecha de compra', 'Fecha de renovación']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    listaImpresoras = []
    listaDepartamentos = []
    infoRenovaciones = Renovacion_Impresoras.objects.all()
        
    for renovacion in infoRenovaciones:
        id_impresora_renov = renovacion.id_impresora_id
        
        infoImpresora = Impresoras.objects.filter(id_impresora = id_impresora_renov)
        
        for dato in infoImpresora:
            marca = dato.marca
            modelo = dato.modelo
            
            areaImp = dato.id_area_id
            
            datosArea = Areas.objects.filter(id_area = areaImp)
                
            for d in datosArea:
                departamento = d.nombre
            
            impresora = marca + " " + modelo
            
            listaImpresoras.append(impresora)
            listaDepartamentos.append(departamento)
    #lista la lista de impresoras, incluyendo sus areas.
        
    renovaciones = Renovacion_Impresoras.objects.all()
    
    datosRenovaviones = []
    cont=0
    for x in renovaciones:
        cont= cont + 1
        datosRenovaviones.append([x.id_impresora_id, listaImpresoras[cont-1], listaDepartamentos[cont-1], 
                             x.fecha_compra, x.fecha_renov])
            
        
    estilo_fuente = xlwt.XFStyle()
    for renovacionsita in datosRenovaviones:
        numero_fila+=1
        for columna in range(len(renovacionsita)):
            hoja.write(numero_fila, columna, str(renovacionsita[columna]), estilo_fuente)

    libro.save(response)
    return response    
    #creación 
    
    
def xlInsumos(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Insumos'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Insumos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Cartucho','Marca', 'Modelo', 'Cantidad', 'N° de serue', 'Color', 'Impresora']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    impresorasss = []
    infoInsumos = Cartuchos.objects.all()
        
    for cartucho in infoInsumos:
        id_impresoraCart = cartucho.id_impresora_id
            
        infoImpresora = Impresoras.objects.filter(id_impresora = id_impresoraCart)#filtro de los empleados que esten dentro de un area especifica
            
        for dato in infoImpresora:
            marca = dato.marca
            modelo = dato.modelo
            
        impresora = marca + " " + modelo
            
        impresorasss.append(impresora)
    
    #lista la lista de impresoras
        
    insumos = Cartuchos.objects.all()
    
    datosInsumos = []
    cont=0
    color = ""
    for x in insumos:
        cont+=1
        datosInsumos.append([x.id_cartucho, x.marca, x.modelo, x.cantidad, x.nuserie, x.color, impresorasss[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for ins in datosInsumos:
        numero_fila+=1
        for columna in range(len(ins)):
            hoja.write(numero_fila, columna, str(ins[columna]), estilo_fuente)
        
    libro.save(response)
    return response

def correoContra(request):
    
     if request.method == "POST":
        
        idEmpleado= request.POST['idEmpleadoContra'] #A o I
        empleadoDatos = Empleados.objects.filter(id_empleado=idEmpleado)
        
        for empleado in empleadoDatos:
            nombre= empleado.nombre
            apellidos=empleado.apellidos
            correo=empleado.correo
            contraseña=empleado.contraseña
            
        asunto = "CS | Solicitud de contraseña de " + nombre + " " + apellidos
        plantilla = "Empleados/correo.html"
        html_mensaje = render_to_string(plantilla, {"nombre": nombre, "apellidos": apellidos, "correo": correo, "contraseña": contraseña})
        email_remitente = settings.EMAIL_HOST_USER
        email_destino = ['sistemas@customco.com.mx']
        mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
        mensaje.content_subtype = 'html'
        mensaje.send()
        
        textoCorreo = "Se ha enviado un correo con la información solicitada."
        request.session['textoCorreo'] = textoCorreo
        return redirect('/verEmpleados/')
        #return redirect('/verEmpleados/')

#Fin, todooo tiene un fiiiiiin

def verMouses(request):
    
    if "idSesion" in request.session:

        estaEnVerMouses = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Listas a utilizar
        mousesActivos = []
        mousesStock = []
        mousesActivosPrestamo = []
        idsMousesPrestados = []
        
        #Lista de todos los mouses
        listaMouses = Mouses.objects.all()
        mousesPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Mouses")
        for dato in mousesPrestados:
            idM = dato.id_producto
            idsMousesPrestados.append(idM)

        
        for mouse in listaMouses:
            idMouse = str(mouse.id_mouse)
            conexion = mouse.conexion
            marca = mouse.marca
            modelo = mouse.modelo
            estado = mouse.estado
            fotoMouse = mouse.foto
            if mouse.id_equipo_id == None:
                tieneequipo = False
            else:
                tieneequipo = True
                idEquipo = mouse.id_equipo_id
            activo = mouse.activo
          

            
            
            if activo == "A":
                 #sacar info de equipo ya que el mouse se encuentra activo
                if tieneequipo == True:
               
                    infoEquipo = Equipos.objects.filter(id_equipo = idEquipo)
              
                    for dato in infoEquipo:
                        idEquipo = str(dato.id_equipo)
                        tipo = dato.tipo
                        marcapc = dato.marca
                        modelopc = dato.modelo 
                            

                            
                        modeloEquipo = "#"+idEquipo + " " + tipo + " " + marcapc + " " + modelopc
                            
                        #datos Empleado de equipo
                        idEmpleado = dato.id_empleado_id
                        infoEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in infoEmpleado:
                            nombre = datoEmpleado.nombre
                            apellidos = datoEmpleado.apellidos
                        empleado = nombre + " " + apellidos
                elif tieneequipo == False:
                    modeloEquipo = "Sin equipo asignado"
                    empleado = "Sin empleado asignado"
                        
                mousesActivos.append([idMouse, conexion, marca, modelo, estado, fotoMouse, modeloEquipo, empleado])

                if idMouse in idsMousesPrestados:
                    for datos in mousesPrestados:
                        idsMPres = datos.id_producto
                        if idMouse == idsMPres:
                            fechaEn = datos.fecha_prestamo
                            firmaEn = datos.firma_entrega

                        mousesActivosPrestamo.append([fechaEn,firmaEn])
                else:
                    mousesActivosPrestamo.append("Sin prestamo")
                
            lista = zip(mousesActivos, mousesActivosPrestamo)


                


            #No tiene un equipo asignado, puede variar el estado..
            
            if activo == "I":
                mousesStock.append([idMouse, conexion, marca, modelo, estado, fotoMouse])
        
        if "idMouseBaja" in request.session:
            baja = True
            mensaje = "Se dio de baja al mouse " + request.session['idMouseBaja']
            del request.session["idMouseBaja"]
            return render(request, "Sistemas/Mouses/verMouses.html", {"estaEnVerMouses":estaEnVerMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mousesActivos":mousesActivos, "mousesStock":mousesStock,
        "mousesActivosPrestamo":mousesActivosPrestamo, "lista":lista, "mousesPrestados":mousesPrestados, "baja":baja, "mensaje":mensaje})

        if "idMouseAlta" in request.session:
            alta = True
            mensaje = "Se dio de alta al mouse " + request.session['idMouseAlta']
            del request.session["idMouseAlta"]
            return render(request, "Sistemas/Mouses/verMouses.html", {"estaEnVerMouses":estaEnVerMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mousesActivos":mousesActivos, "mousesStock":mousesStock,
        "mousesActivosPrestamo":mousesActivosPrestamo, "lista":lista, "mousesPrestados":mousesPrestados, "alta":alta, "mensaje":mensaje})

        if "mouseEditado" in request.session:
            editado = True
            mensaje = request.session["mouseEditado"]
            del request.session["mouseEditado"]
            return render(request, "Sistemas/Mouses/verMouses.html", {"estaEnVerMouses":estaEnVerMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mousesActivos":mousesActivos, "mousesStock":mousesStock,
        "mousesActivosPrestamo":mousesActivosPrestamo, "lista":lista, "mousesPrestados":mousesPrestados, "editado":editado, "mensaje":mensaje})
            
           

     
                
                    
                    
                
                
                
            
        
        
        

        return render(request, "Sistemas/Mouses/verMouses.html", {"estaEnVerMouses":estaEnVerMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mousesActivos":mousesActivos, "mousesStock":mousesStock,
        "mousesActivosPrestamo":mousesActivosPrestamo, "lista":lista, "mousesPrestados":mousesPrestados})
                                                                  
    else:
        return redirect('/login/') #redirecciona a url de inicio

def bajaMouse(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idBaja= request.POST['idMouseBaja']
            
            datosMouse = Mouses.objects.filter(id_mouse = idBaja)
            estadoB = ""
            
            for dato in datosMouse:
                idMouse = str(dato.id_mouse)
                marca = dato.marca
                modelo = dato.modelo
                estado = dato.estado
                
            

            
            nombreCompletoMouse = marca + " " + modelo
           

            actualizacion = Mouses.objects.filter(id_mouse = idMouse).update(activo = "I", estado = "stockUsado", id_equipo = "")

            if actualizacion:
                    
                request.session['idMouseBaja'] = nombreCompletoMouse
                prestamo =  PrestamosSistemas.objects.filter(id_producto = idBaja, tabla = "Mouses")

                if prestamo:
                    mouse = int(idBaja)
                    borrado = PrestamosSistemas.objects.get(id_producto = mouse, tabla = "Mouses")
                    borrado.delete()
                    
                return redirect('/verMouses/')

               
                
                            
            
  
            
    else:
        return redirect('/login/') #redirecciona a url de inicio

   
def altaMouse(request):
    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idAlta= request.POST['idMouseAlta']
            idsMousesP =[]
            datosMouse = Mouses.objects.filter(id_mouse = idAlta)
            
            for dato in datosMouse:
                idMouse = str(dato.id_mouse)
                marca = dato.marca
                modelo = dato.modelo
  
            nombreCompletoMouse = marca + " " + modelo

            mousesPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Mouses")
            for dato in mousesPrestados:
                idM = dato.id_producto
                idsMousesP.append(idM)

      

            
            actualizacion = Mouses.objects.filter(id_mouse = idAlta).update(activo = "A", estado = "activoFuncional")
            if actualizacion:
                            
                                
                            
                request.session['idMouseAlta'] = nombreCompletoMouse
                                
                return redirect('/verMouses/')
    else:
        return redirect('/login/') #redirecciona a url de inicio

def agregarMouses(request):
    
    if "idSesion" in request.session:

        estaEnAgregarMouses = True
        registroMouseCompletado = False
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Carga de todos los equipos para el select
        equipos = Equipos.objects.all()
        
        #Si se le dio clic al botón de Guardar Mouse
        if request.method == "POST":
            
            marcaMouse = request.POST['marcaMouse']
            modeloMouse = request.POST['modeloMouse']
            tipoConexion = request.POST['tipoCon']
            estadoMouse = request.POST['estado']
            imagenMouse = request.FILES.get('imagenMouse')
            equipoMouse = request.POST['equipo']
            
            #Si el mouse fue guardado sin equipo..
            if equipoMouse == "SinEquipo":
                registroMouse = Mouses(conexion = tipoConexion, marca = marcaMouse, modelo = modeloMouse, 
                                       estado = estadoMouse, foto = imagenMouse, activo = "I")
                registroMouse.save()
            
            #Si el mouse se guardó con un equipo...
            elif equipoMouse != "SinEquipo":
                registroMouse = Mouses(conexion = tipoConexion, marca = marcaMouse, modelo = modeloMouse, 
                                       estado = estadoMouse, foto = imagenMouse, id_equipo = Equipos.objects.get(id_equipo = equipoMouse),activo = "A")
                registroMouse.save()
            
            #Variables para el mensaje
            if registroMouse:
                registroMouseCompletado = True
                texto  = "Se ha registrado el mouse "+ marcaMouse + " " + modeloMouse
                
            return render(request, "Sistemas/Mouses/agregarMouses.html", {"estaEnAgregarMouses":estaEnAgregarMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "equipos":equipos, 
                                                                          "registroMouseCompletado":registroMouseCompletado, "texto":texto})

        





        return render(request, "Sistemas/Mouses/agregarMouses.html", {"estaEnAgregarMouses":estaEnAgregarMouses,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "equipos":equipos, 
                                                                      "registroMouseCompletado":registroMouseCompletado})
    else:
        return redirect('/login/') #redirecciona a url de inicio

    
def editarMouse(request):
    
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            mouseRecibido = request.POST['idMouseEditar']
            mouseDatos = Mouses.objects.filter(id_mouse=mouseRecibido)

            equipoEmpleados = []
            for dato in mouseDatos:
                equipoId= dato.id_equipo_id #2
                estado = dato.estado

            equiposM = Equipos.objects.filter(id_equipo= equipoId)
            for equ in equiposM:
                id_empleadoM = equ.id_empleado_id
              
               
                
            if equipoId == None:

                estados = ["activoFuncional", "stockUsado", "stockNuevo", "basura"]
                for es in estados:
                    if es == estado:
                        estados.remove(es)

                
                
               
                equiposTotales = Equipos.objects.all()
                for eT in equiposTotales:
                    idEq = eT.id_equipo
                    marcaEq = eT.marca
                    modeloEq = eT.modelo
                    idEmpl = eT.id_empleado_id
                    empleadosTotales = Empleados.objects.filter(id_empleado = idEmpl)
                    for emple in empleadosTotales:
                        nombreE = emple.nombre
                        apellidosE = emple.apellidos
                    completo = str (idEq) + " " + " " + marcaEq + " " + modeloEq  + "de: " + nombreE + " " + apellidosE
                    equipoEmpleados.append(completo)

                

                
                    
                sinEquipo = True
                lista = zip(mouseDatos,equiposTotales)
                return render(request, "Editar/editarMouse.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista,"estados":estados, "mouseRecibido":mouseRecibido, "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                    "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                equiposM = Equipos.objects.filter(id_equipo = equipoId)
                for eqE in equiposM:
                    id_empleadoE = eqE.id_empleado_id 

                empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
                for de in empleadoDe:
                    nombres = de.nombre
                    apell = de.apellidos
                                    

               
               
                            
                estados = ["activoFuncional", "stockUsado", "stockNuevo", "basura"]
                for es in estados:
                    if es == estado:
                        estados.remove(es)

                
                lista = zip(mouseDatos,equiposM)
                
                equipos_totales = Equipos.objects.all()
                arreglo_ids = []
                
                for equi in equipos_totales:
                    arreglo_ids.append(equi.id_equipo)
                
                #[1,2,3]
                
                for id in arreglo_ids:
                    if id == equipoId: #si 2 == 2
                        arreglo_ids.remove(id)
                        
                #[1,3]
                
                datos_equipo = []
                
                for id in arreglo_ids:
                    datos = Equipos.objects.filter(id_equipo = id)
                    for dato in datos:
                        id_equipo = dato.id_equipo
                        tipo = dato.tipo
                        marca = dato.marca
                        modelo = dato.modelo
                        foto = dato.imagen
                        id_empleado = dato.id_empleado_id
                    datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                    empleados = Empleados.objects.filter(id_empleado = id_empleado)
                    for em in empleados:
                        nombree = em.nombre
                        apellidose = em.apellidos

           
                
                

                    
                        
                
            
            return render(request, "Editar/editarMouse.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "estados":estados,  "equiposM":equiposM, "equipos_totales":equipos_totales, "empleadoDe":empleadoDe, "mouseRecibido":mouseRecibido, "datos_equipo":datos_equipo, "empleados":empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        return render(request, "Editar/editarMouse.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

   
def editarMouseBd(request):
    
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            mouseId = request.POST['idMouse']
            equipo_actualizar = request.POST['equipo']
            estado_actualizar = request.POST['estado']
         

            
            if equipo_actualizar == "sinEquipo":
                actualizar = Mouses.objects.filter(id_mouse=mouseId).update( id_equipo_id=None,estado= estado_actualizar, activo="I")
                
                
            elif equipo_actualizar !=  "sinEquipo": 
                int_equipo = int(equipo_actualizar)
                actualizar = Mouses.objects.filter(id_mouse=mouseId).update( id_equipo_id=Equipos.objects.get(id_equipo = int_equipo),
                                                 estado= estado_actualizar, activo="A")
            
            datosMouse = Mouses.objects.filter(id_mouse = mouseId)
                
            for dato in datosMouse:
                conexion = dato.conexion
                marca = dato.marca
                modelo = dato.modelo
                    
            todoMouse = conexion + " " + marca + " " + modelo

            if actualizar:

                textoEdicion = "Se ha editado al mouse " + todoMouse + " con éxito!"
                
                prestamo =  PrestamosSistemas.objects.filter(id_producto = mouseId, tabla = "Mouses")

                if prestamo:
                    mouse = int(mouseId)
                    borrado = PrestamosSistemas.objects.get(id_producto = mouse, tabla = "Mouses")
                    borrado.delete()    

                #Variable de sesion para notificacion
                request.session['mouseEditado'] = textoEdicion

                return redirect('/verMouses/')
                
                

            
        return render(request,"Editar/editarEmpleado.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def correoContra(request):
    
     if request.method == "POST":
        
        idEmpleado= request.POST['idEmpleadoContra'] #A o I
        empleadoDatos = Empleados.objects.filter(id_empleado=idEmpleado)
        
        for empleado in empleadoDatos:
            nombre= empleado.nombre
            apellidos=empleado.apellidos
            correo=empleado.correo
            contraseña=empleado.contraseña
            
        asunto = "CS | Solicitud de contraseña de " + nombre + " " + apellidos
        plantilla = "Empleados/correo.html"
        html_mensaje = render_to_string(plantilla, {"nombre": nombre, "apellidos": apellidos, "correo": correo, "contraseña": contraseña})
        email_remitente = settings.EMAIL_HOST_USER
        email_destino = ['sistemas@customco.com.mx']
        mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
        mensaje.content_subtype = 'html'
        mensaje.send()
        
        textoCorreo = "Se ha enviado un correo con la información solicitada."
        request.session['textoCorreo'] = textoCorreo
        return redirect('/verEmpleados/')
        #return redirect('/verEmpleados/')

#Fin, todooo tiene un fiiiiiin

def verTeclados(request):
    
    if "idSesion" in request.session:

        estaEnVerTeclados = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        #arreglos para almacenar teclados activos e inactivos

        tecladosActivos = []
        tecladosStock = []
        tecladosActivosPrestamos = []
        idsTecladosPrestamos = []


        #LISTA DE TODOS LOS TECLADOS 
        teclados = Teclados.objects.all()

        tecladosPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Teclados")
        for te in tecladosPrestados:
            idT = te.id_producto
            idsTecladosPrestamos.append(idT)



        #obtener los datos de cada uno de los teclados

        for tecla in teclados:
            idTeclado = str(tecla.id_teclado)
            tipoCon = tecla.conexion
            marcaTeclado = tecla.marca
            modeloTeclado = tecla.modelo
            estadoTeclado = tecla.estado
            fotoTeclado = tecla.foto
            if tecla.id_equipo_id == None:
                ConEquipo = False
            else:
                ConEquipo = True

            
                equipoPertenece = str(tecla.id_equipo_id)
            activoTeclado = tecla.activo

            if activoTeclado == "A":

                if ConEquipo == True:
                    #obtener los datos del equipo al que pertenece
                    equipoDatos = Equipos.objects.filter(id_equipo = int(equipoPertenece))
                    for dato in equipoDatos:
                        idEquipo = str(dato.id_equipo)
                        tipo = dato.tipo
                        marca = dato.marca
                        modelo = dato.modelo

                        infoEquipo = "#"+ " " + idEquipo + " " + tipo + " " + marca + " " + modelo

                        #Obtener los datos del empleado al que pertenece
                        idPropietario = str(dato.id_empleado_id)
                        datosEmpleado = Empleados.objects.filter(id_empleado= int(idPropietario))
                        for datos in datosEmpleado:
                            propietario = str(datos.id_empleado)
                            nombres = datos.nombre
                            apellido = datos.apellidos

                        infoPropietario = "#" + " " + propietario + " " + nombres + " " + apellido
                elif ConEquipo == False:
                    infoEquipo = "Sin equipo"
                    infoPropietario = "Sin propietario"

                    
                tecladosActivos.append([idTeclado, tipoCon, marcaTeclado, modeloTeclado, estadoTeclado, fotoTeclado, infoEquipo, infoPropietario])

                if idTeclado in idsTecladosPrestamos:
                    for tecl in tecladosPrestados:
                        idTP = tecl.id_producto
                        if idTeclado == idTP:
                            fechaPrestamo = tecl.fecha_prestamo
                            firmaEntrega = tecl.firma_entrega
                        tecladosActivosPrestamos.append([fechaPrestamo, firmaEntrega])

                 
                else:
                    tecladosActivosPrestamos.append("Sin prestamo")
                
            lista = zip(tecladosActivos, tecladosActivosPrestamos)

                

            #si esta en stock (inactivo)

            if activoTeclado == "I":
                tecladosStock.append([idTeclado, tipoCon, marcaTeclado, modeloTeclado, estadoTeclado, fotoTeclado])

            if "idTecladoBaja" in request.session:
                baja = True
                mensaje = "Se dio de baja al teclado " + request.session['idTecladoBaja']
                del request.session["idTecladoBaja"]
                return render(request, "Sistemas/Teclados/verTeclados.html", {"estaEnVerTeclados":estaEnVerTeclados,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"tecladosActivos":tecladosActivos, "tecladosStock":tecladosStock,
            "tecladosActivosPrestamos":tecladosActivosPrestamos, "lista":lista, "tecladosPrestados":tecladosPrestados, "baja":baja, "mensaje":mensaje})

            if "idTecladoAlta" in request.session:
                alta = True
                mensaje = "Se dio de alta al teclado " + request.session['idTecladoAlta']
                del request.session["idTecladoAlta"]
                return render(request, "Sistemas/Teclados/verTeclados.html", {"estaEnVerTeclados":estaEnVerTeclados,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"tecladosActivos":tecladosActivos, "tecladosStock":tecladosStock,
            "tecladosActivosPrestamos":tecladosActivosPrestamos, "lista":lista, "tecladosPrestados":tecladosPrestados, "alta":alta, "mensaje":mensaje})




        return render(request, "Sistemas/Teclados/verTeclados.html", {"estaEnVerTeclados":estaEnVerTeclados,"id_admin":id_admin, "lista":lista, "tecladosActivosPrestamos":tecladosActivosPrestamos,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
                                                                    "tecladosActivos": tecladosActivos, "tecladosStock": tecladosStock})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def bajaTeclado(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idBaja= request.POST['idTecladoBaja']
            
            datosTeclado = Teclados.objects.filter(id_teclado = idBaja)
            
            
            for dato in datosTeclado:
                idTeclado = str(dato.id_teclado)
                marca = dato.marca
                modelo = dato.modelo
            
                
            

            
            nombreCompletoTeclado = marca + " " + modelo
           

            actualizacion = Teclados.objects.filter(id_teclado = idTeclado).update(activo = "I", estado = "stockUsado", id_equipo = "")

            if actualizacion:
                    
                request.session['idTecladoBaja'] = nombreCompletoTeclado
                prestamo =  PrestamosSistemas.objects.filter(id_producto = idBaja)

                if prestamo:
                    teclado = int(idBaja)
                    borrado = PrestamosSistemas.objects.get(id_producto = teclado, tabla = "Teclados")
                    borrado.delete()
                    
                return redirect('/verTeclados/')

               
                
                            
            
  
            
    else:
        return redirect('/login/') #redirecciona a url de inicio

def altaTeclado(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idAlta= request.POST['idTecladoAlta']
            idsTecladoP =[]
            datosTeclado = Teclados.objects.filter(id_teclado = idAlta)
            
            for dato in datosTeclado:
                idTeclado = str(dato.id_teclado)
                marca = dato.marca
                modelo = dato.modelo
  
            nombreCompletoTeclado = marca + " " + modelo

            tecladosPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Teclados")
            for dato in tecladosPrestados:
                idT = dato.id_producto
                idsTecladoP.append(idT)

      

            
            actualizacion = Teclados.objects.filter(id_teclado = idAlta).update(activo = "A", estado = "activoFuncional")
            if actualizacion:
                            
                                
                            
                request.session['idTecladoAlta'] = nombreCompletoTeclado
                                
                return redirect('/verTeclados/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def agregarTeclados(request):
    
    if "idSesion" in request.session:

        estaEnAgregarTeclados = True
        registroTecladoCompleto = False
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        #Carga de todos los equipos para el select
        equipos = Equipos.objects.all()
        
        #Si se le dio clic al botón de Guardar tecldo
        if request.method == "POST":
            
            marcaTeclado = request.POST['marcaTeclado']
            modeloTeclado = request.POST['modeloTeclado']
            tipoConexion = request.POST['conexionTeclado']
            estadoTeclado = request.POST['estadoTeclado']
            imagenTeclado = request.FILES.get('imagenTeclado')
            equipoTeclado = request.POST['equipoTec']
            
            #Si el teclado fue guardado sin equipo..
            if equipoTeclado == "SinEquipo":
                registroTeclado = Teclados(conexion = tipoConexion, marca = marcaTeclado, modelo = modeloTeclado, 
                                       estado = estadoTeclado, foto = imagenTeclado, activo = "I")
                registroTeclado.save()
            
            #Si el teclado se guardó con un equipo...
            elif equipoTeclado != "SinEquipo":
                registroTeclado = Teclados(conexion = tipoConexion, marca = marcaTeclado, modelo = modeloTeclado, 
                                       estado = estadoTeclado, foto = imagenTeclado, id_equipo = Equipos.objects.get(id_equipo = equipoTeclado),activo = "A")
                registroTeclado.save()
            
            #Variables para el mensaje
            if registroTeclado:
                registroTecladoCompleto = True
                texto  = "Se ha registrado el teclado "+ marcaTeclado + " " + modeloTeclado
                
            return render(request, "Sistemas/Teclados/agregarTeclados.html", {"estaEnAgregarTeclados":estaEnAgregarTeclados,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "equipos":equipos, 
                                                                          "registroTecladoCompleto":registroTecladoCompleto, "texto":texto})


        return render(request, "Sistemas/Teclados/agregarTeclados.html", {"estaEnAgregarTeclados":estaEnAgregarTeclados,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "equipos":equipos, 
                                                                          "registroTecladoCompleto":registroTecladoCompleto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def editarTeclado(request):
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            tecladoRecibido = request.POST['idTecladoEditar']
            tecladoDatos = Teclados.objects.filter(id_teclado=tecladoRecibido)

           
            for dato in tecladoDatos:
                equipoId= dato.id_equipo_id #2
           

            equiposT = Equipos.objects.filter(id_equipo= equipoId)
       
              
               
                
            if equipoId == None:


                equiposTotales = Equipos.objects.all()
 
                    
                sinEquipo = True
                lista = zip(tecladoDatos,equiposTotales)
                return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "equiposT":equiposT, "lista":lista, "tecladoRecibido":tecladoRecibido, "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                    "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                equiposT = Equipos.objects.filter(id_equipo = equipoId)
                for eqE in equiposT:
                    id_empleadoE = eqE.id_empleado_id 

                empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
               
     
                
                lista = zip(tecladoDatos,equiposT)
                
                equipos_totales = Equipos.objects.all()
                arreglo_ids = []
                
                for equi in equipos_totales:
                    arreglo_ids.append(equi.id_equipo)
                
                #[1,2,3]
                
                for id in arreglo_ids:
                    if id == equipoId: #si 2 == 2
                        arreglo_ids.remove(id)
                        
                #[1,3]
                
                datos_equipo = []
                
                for id in arreglo_ids:
                    datos = Equipos.objects.filter(id_equipo = id)
                    for dato in datos:
                        id_equipo = dato.id_equipo
                        tipo = dato.tipo
                        marca = dato.marca
                        modelo = dato.modelo
                        foto = dato.imagen
                        id_empleado = dato.id_empleado_id
                    datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        
                
            
            return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "equiposT":equiposT, "equipos_totales":equipos_totales, "empleadoDe":empleadoDe, "datos_equipo":datos_equipo, "empleadoDe":empleadoDe, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def editarTecladoBd(request):
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            tecladoId = request.POST['idTeclado']
            equipo_actualizar = request.POST['equipo']
            estado_actualizar = request.POST['estado']
         

            
            if equipo_actualizar == "sinEquipo":
                actualizar = Teclados.objects.filter(id_teclado=tecladoId).update( id_equipo_id=None,estado= estado_actualizar, activo="I")
                
                
            elif equipo_actualizar !=  "sinEquipo": 
                int_equipo = int(equipo_actualizar)
                actualizar = Teclados.objects.filter(id_teclado=tecladoId).update( id_equipo_id=Equipos.objects.get(id_equipo = int_equipo),
                                                 estado= estado_actualizar, activo="A")
            
            if actualizar:
               
                datos = Teclados.objects.filter(id_teclado = tecladoId)
            

                
                for dato in datos:
                    conexion = dato.conexion
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoTeclado = conexion + " " + marca + " " + modelo
                
                
                
                editado = True
                textoEdicion = "Se ha editado al teclado " + todoTeclado + " con éxito!"
              
                
               
                

                tecladoRecibido = tecladoId
                tecladoDatos = Teclados.objects.filter(id_teclado=tecladoRecibido)

                
                for dato in tecladoDatos:
                    equipoId= dato.id_equipo_id #2
                    estado = dato.estado
                    
                if equipoId == None:
                    

                    equiposTotales = Equipos.objects.all()
                            
               
                    
                        
                    sinEquipo = True
                    lista = zip(tecladoDatos,equiposTotales)

                    prestamo =  PrestamosSistemas.objects.filter(id_producto = tecladoId)

                    if prestamo:
                        teclado = int(tecladoId)
                        borrado = PrestamosSistemas.objects.get(id_producto = teclado, tabla = "Teclados")
                        borrado.delete()
                                
                        return redirect('/verTeclados/')


                    return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "tecladoRecibido":tecladoRecibido, "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    equiposT = Equipos.objects.filter(id_equipo = equipoId)
                    for eqE in equiposT:
                        id_empleadoE = eqE.id_empleado_id 

                    empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
                    for de in empleadoDe:
                        nombres = de.nombre
                        apell = de.apellidos


                    lista = zip(tecladoDatos, equiposT)
                    
                    equipos_totales = Equipos.objects.all()
                    arreglo_ids = []
                
                    for equi in equipos_totales:
                        arreglo_ids.append(equi.id_equipo)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == equipoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                    datos_equipo = []
                    datos_empleados = []
                    
                    for id in arreglo_ids:
                        datos = Equipos.objects.filter(id_equipo = id)
                        for dato in datos:
                            id_equipo = dato.id_equipo
                            tipo = dato.tipo
                            marca = dato.marca
                            modelo = dato.modelo
                            foto = dato.imagen
                            id_empleado = dato.id_empleado_id
                        datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        empleados = Empleados.objects.filter(id_empleado = id_empleado)
                       
                        

                  
                    return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "empleadoDe":empleadoDe, "equipos_totales":equipos_totales, "correo":correo, "lista":lista, "equiposT":equiposT, "empleados":empleados, "datos_equipo":datos_equipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                datos = Teclados.objects.filter(id_teclado = tecladoId)

                
                for dato in datos:
                    conexion = dato.conexion
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoTeclado = conexion + " " + marca + " " + modelo
                
                
                editado = True
                textoEdicion = "Error en la base de datos!"
               
             
                tecladoRecibido = tecladoId
                tecladoDatos = Teclados.objects.filter(id_teclado=tecladoRecibido)

                
                for dato in tecladoDatos:
                    equipoId= dato.id_equipo_id #2
                    estadomou = dato.estado
                    
                    
                if equipoId == None:
                  

                
                
               
                    equiposTotales = Equipos.objects.all()
                        
                    
                        
                    sinEquipo = True
                    lista = zip(tecladoDatos,equiposTotales)
                    return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "tecladoRecibido":tecladoRecibido,  "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    equiposT = Equipos.objects.filter(id_equipo = equipoId)
                    for eqE in equiposT:
                        id_empleadoE = eqE.id_empleado_id 

                    empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
                

                    lista = zip(tecladoDatos, equiposTotales)
                    
                    equipos_totales = Equipos.objects.all()
                    arreglo_ids = []
                
                    for equi in equipos_totales:
                        arreglo_ids.append(equi.id_equipo)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == equipoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                    datos_equipo = []
                
                    
                    for id in arreglo_ids:
                        datos = Equipos.objects.filter(id_equipo = id)
                        for dato in datos:
                            id_equipo = dato.id_equipo
                            tipo = dato.tipo
                            marca = dato.marca
                            modelo = dato.modelo
                            foto = dato.imagen
                            id_empleado = dato.id_empleado_id
                        datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        empleados = Empleados.objects.filter(id_empleado = id_empleado)
                       
                        

                  
                    return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "empleadoDe":empleadoDe, "equipos_totales":equipos_totales, "correo":correo, "lista":lista, "equiposT":equiposT, "empleados":empleados, "datos_equipo":datos_equipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    
        return render(request,"Editar/editarEmpleado.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio   

def verMonitores(request):
    
    if "idSesion" in request.session:

        estaEnVerMonitores = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Listas a utilizar
        monitoresActivos = []
        monitoresStock = []
        monitoresActivosPrestamos = []
        idsMonitoresPrestamos = []
        
        #Lista de todos los mouses
        listaMonitores = Monitores.objects.all()
        monitoresPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Monitores")
        for monP in monitoresPrestados:
            idMon = monP.id_producto
            idsMonitoresPrestamos.append(idMon)

        
        for monitor in listaMonitores:
            idMonitor = str(monitor.id_monitor)
            marca = monitor.marca
            modelo = monitor.modelo
            estado = monitor.estado
            fotoMouse = monitor.foto
            if monitor.id_equipo_id == None:
                ConEquipo = False

            else:
                ConEquipo = True
                idEquipo = str(monitor.id_equipo_id)
            activo = monitor.activo
            
            if activo == "A":
                if ConEquipo == True:
                     
                    #sacar info de equipo ya que el mouse se encuentra activo
                    infoEquipo = Equipos.objects.filter(id_equipo = int(idEquipo))
                    for dato in infoEquipo:
                        idEquipo = str(dato.id_equipo)
                        tipo = dato.tipo
                        marcapc = dato.marca
                        modelopc = dato.modelo 
                        
                        modeloEquipo = "#"+idEquipo + " " + tipo + " " + marcapc + " " + modelopc
                        
                        #datos Empleado de equipo
                        idEmpleado = dato.id_empleado_id
                        infoEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in infoEmpleado:
                            nombre = datoEmpleado.nombre
                            apellidos = datoEmpleado.apellidos
                        empleado = nombre + " " + apellidos

                elif ConEquipo == False:
                    modeloEquipo = "Sin equipo"
                    empleado = "Sin propietario"
                        
                monitoresActivos.append([idMonitor, marca, modelo, estado, fotoMouse, modeloEquipo, empleado])

                if idMonitor in idsMonitoresPrestamos:
                    for monitorP in monitoresPrestados:
                        idMonitorP = monitorP.id_producto
                        if idMonitor == idMonitorP:
                            fechaEntrega = monitorP.fecha_prestamo
                            firmaEn = monitorP.firma_entrega
                        
                        monitoresActivosPrestamos.append([fechaEntrega, firmaEn])
                else:
                    monitoresActivosPrestamos.append("Sin prestamo")
                
            lista = zip(monitoresActivos, monitoresActivosPrestamos)

                
                            





            #No tiene un equipo asignado, puede variar el estado..
            
            if activo == "I":
                monitoresStock.append([idMonitor, marca, modelo, estado, fotoMouse])

            
            if "idMonitorBaja" in request.session:
                baja = True
                mensaje = "Se dio de baja al monitor " + request.session['idMonitorBaja']
                del request.session["idMonitorBaja"]
                return render(request, "Sistemas/Monitores/verMonitores.html", {"estaEnVerMonitores":estaEnVerMonitores,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"monitoresActivos":monitoresActivos, "monitoresStock":monitoresStock,
            "monitoresActivosPrestamos":monitoresActivosPrestamos, "lista":lista, "idsMonitoresPrestamos":idsMonitoresPrestamos, "baja":baja, "mensaje":mensaje})

            if "idMonitorBaja" in request.session:
                alta = True
                mensaje = "Se dio de alta al monitor " + request.session['idMonitorBaja']
                del request.session["idMonitorBaja"]
                return render(request, "Sistemas/Monitores/verMonitores.html", {"estaEnVerMonitores":estaEnVerMonitores,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"monitoresActivos":monitoresActivos, "monitoresStock":monitoresStock,
            "monitoresActivosPrestamos":monitoresActivosPrestamos, "lista":lista, "idsMonitoresPrestamos":idsMonitoresPrestamos, "alta":alta, "mensaje":mensaje})

        return render(request, "Sistemas/Monitores/verMonitores.html", {"estaEnVerMonitores":estaEnVerMonitores,"id_admin":id_admin, "lista":lista, "monitoresActivosPrestamos":monitoresActivosPrestamos, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "monitoresActivos":monitoresActivos, "monitoresStock":monitoresStock})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def bajaMonitor(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idBaja= request.POST['idMonitorBaja']
            
            datosMonitor = Monitores.objects.filter(id_monitor = idBaja)
            
            
            for dato in datosMonitor:
                idMonitor = str(dato.id_monitor)
                marca = dato.marca
                modelo = dato.modelo
            
                
        

            
            nombreCompletoMonitor = marca + " " + modelo
           

            actualizacion = Monitores.objects.filter(id_monitor = idMonitor).update(activo = "I", estado = "stockUsado", id_equipo = "")

            if actualizacion:
                    
                request.session['idMonitorBaja'] = nombreCompletoMonitor
                prestamo =  PrestamosSistemas.objects.filter(id_producto = idBaja)

                if prestamo:
                    monitor = int(idBaja)
                    borrado = PrestamosSistemas.objects.get(id_producto = monitor, tabla = "Monitores")
                    borrado.delete()
                    
                return redirect('/verMonitores/')

               
                
                            
            
  
            
    else:
        return redirect('/login/') #redirecciona a url de inicio

def altaMonitor(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idAlta= request.POST['idMonitorAlta']
            idsMonitorP =[]
            datosMonitor = Monitores.objects.filter(id_monitor = idAlta)
            
            for dato in datosMonitor:
                idMonitor = str(dato.id_monitor)
                marca = dato.marca
                modelo = dato.modelo
  
            nombreCompletoMonitor = marca + " " + modelo

            monitoresPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Monitores")
            for dato in monitoresPrestados:
                idT = dato.id_producto
                idsMonitorP.append(idT)

      

            
            actualizacion = Monitores.objects.filter(id_monitor = idMonitor).update(activo = "A", estado = "activoFuncional")
            if actualizacion:
                            
                                
                            
                request.session['idMonitorAlta'] = nombreCompletoMonitor
                                
                return redirect('/verMonitores/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
def agregarMonitores(request):
    
    if "idSesion" in request.session:

        estaEnAgregarMonitores = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #consulta equipos
        equipos = Equipos.objects.all()
        
        #Si se le dio clic al botón de Guardar Monitor
        if request.method == "POST":
            
            marcaMonitor = request.POST['marcaMonitor']
            modeloMonitor = request.POST['modeloMonitor']
            estadoMonitor = request.POST['estadoMonitor']
            imagenMonitor = request.FILES.get('imagenMonitor')
            equipoMonitor = request.POST['equipoMonitor']
            
            #Si el mouse fue guardado sin equipo..
            if equipoMonitor == "SinEquipo":
                registroMonitor = Monitores(marca = marcaMonitor, modelo = modeloMonitor, 
                                       estado = estadoMonitor, foto = imagenMonitor, activo = "I")
                registroMonitor.save()
            
            #Si el mouse se guardó con un equipo...
            elif equipoMonitor != "SinEquipo":
                registroMonitor = Monitores(marca = marcaMonitor, modelo = modeloMonitor, 
                                       estado = estadoMonitor, foto = imagenMonitor, id_equipo = Equipos.objects.get(id_equipo = equipoMonitor),activo = "A")
                registroMonitor.save()
            
            #Variables para el mensaje
            if registroMonitor:
                registroMonitorCompletado = True
                texto  = "Se ha registrado el monitor "+ marcaMonitor + " " + modeloMonitor
                
            return render(request, "Sistemas/Monitores/agregarMonitores.html", {"estaEnAgregarMonitores":estaEnAgregarMonitores,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, 
                                                                            "equipos":equipos, "registroMonitorCompletado":registroMonitorCompletado, "texto":texto})

        

        return render(request, "Sistemas/Monitores/agregarMonitores.html", {"estaEnAgregarMonitores":estaEnAgregarMonitores,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, 
                                                                            "equipos":equipos})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
   
def editarMonitor(request):
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            monitorRecibido = request.POST['idMonitorEditar']
            monitorDatos = Monitores.objects.filter(id_monitor=monitorRecibido)

           
            for dato in monitorDatos:
                equipoId= dato.id_equipo_id #2
           

            equiposMon = Equipos.objects.filter(id_equipo= equipoId)
       
              
               
                
            if equipoId == None:


                equiposTotales = Equipos.objects.all()
 
                    
                sinEquipo = True
                lista = zip(monitorDatos,equiposTotales)
                return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "equiposMon":equiposMon, "lista":lista, "monitorRecibido":monitorRecibido, "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                    "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                equiposMon = Equipos.objects.filter(id_equipo = equipoId)
                for eqE in equiposMon:
                    id_empleadoE = eqE.id_empleado_id 

                empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
               
     
                
                lista = zip(monitorDatos,equiposMon)
                
                equipos_totales = Equipos.objects.all()
                arreglo_ids = []
                
                for equi in equipos_totales:
                    arreglo_ids.append(equi.id_equipo)
                
                #[1,2,3]
                
                for id in arreglo_ids:
                    if id == equipoId: #si 2 == 2
                        arreglo_ids.remove(id)
                        
                #[1,3]
                
                datos_equipo = []
                
                for id in arreglo_ids:
                    datos = Equipos.objects.filter(id_equipo = id)
                    for dato in datos:
                        id_equipo = dato.id_equipo
                        tipo = dato.tipo
                        marca = dato.marca
                        modelo = dato.modelo
                        foto = dato.imagen
                        id_empleado = dato.id_empleado_id
                    datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        
                
            
            return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "equiposMon":equiposMon, "equipos_totales":equipos_totales, "empleadoDe":empleadoDe, "datos_equipo":datos_equipo, "empleadoDe":empleadoDe, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def editarMonitorBd(request):
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            monitorId = request.POST['idMonitor']
            equipo_actualizar = request.POST['equipo']
            estado_actualizar = request.POST['estado']
         

            
            if equipo_actualizar == "sinEquipo":
                actualizar = Monitores.objects.filter(id_monitor=monitorId).update( id_equipo_id=None,estado= estado_actualizar, activo="I")
                
                
            elif equipo_actualizar !=  "sinEquipo": 
                int_equipo = int(equipo_actualizar)
                actualizar = Monitores.objects.filter(id_monitor=monitorId).update( id_equipo_id=Equipos.objects.get(id_equipo = int_equipo),
                                                 estado= estado_actualizar, activo="A")
            
            if actualizar:
               
                datos = Monitores.objects.filter(id_monitor = monitorId)
            

                
                for dato in datos:
               
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoMonitor = marca + " " + modelo
                
                
                
                editado = True
                textoEdicion = "Se ha editado al monitor " + todoMonitor + " con éxito!"
              
                
               
                

                monitorRecibido = monitorId
                monitorDatos = Monitores.objects.filter(id_monitor=monitorRecibido)

                
                for dato in monitorDatos:
                    equipoId= dato.id_equipo_id #2
                    estado = dato.estado
                    
                if equipoId == None:
                    

                    equiposTotales = Equipos.objects.all()
                            
               
                    
                        
                    sinEquipo = True
                    lista = zip(monitorDatos,equiposTotales)

                    prestamo =  PrestamosSistemas.objects.filter(id_producto = monitorId)

                    if prestamo:
                        monitor = int(monitorId)
                        borrado = PrestamosSistemas.objects.get(id_producto = monitor, tabla = "Monitores")
                        borrado.delete()
                            
                        return redirect('/verMonitores/')


                    return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista": lista, "monitorRecibido":monitorRecibido, "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    equiposMon = Equipos.objects.filter(id_equipo = equipoId)
                    for eqE in equiposMon:
                        id_empleadoE = eqE.id_empleado_id 

                    empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
                    for de in empleadoDe:
                        nombres = de.nombre
                        apell = de.apellidos


                    lista = zip(monitorDatos, equiposMon)
                    
                    equipos_totales = Equipos.objects.all()
                    arreglo_ids = []
                
                    for equi in equipos_totales:
                        arreglo_ids.append(equi.id_equipo)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == equipoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                    datos_equipo = []
                    datos_empleados = []
                    
                    for id in arreglo_ids:
                        datos = Equipos.objects.filter(id_equipo = id)
                        for dato in datos:
                            id_equipo = dato.id_equipo
                            tipo = dato.tipo
                            marca = dato.marca
                            modelo = dato.modelo
                            foto = dato.imagen
                            id_empleado = dato.id_empleado_id
                        datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        empleados = Empleados.objects.filter(id_empleado = id_empleado)
                       
                       

                  
                    return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "empleadoDe":empleadoDe, "equipos_totales":equipos_totales, "correo":correo, "lista":lista, "equiposMon":equiposMon, "empleados":empleados, "datos_equipo":datos_equipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                datos = Monitores.objects.filter(id_monitor = monitorId)

                
                for dato in datos:
                 
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoMonitor = marca + " " + modelo
                
                
                editado = True
                textoEdicion = "Error en la base de datos!"
               
             
                monitorRecibido = monitorId
                monitorDatos = Monitores.objects.filter(id_monitor=monitorRecibido)

                
                for dato in monitorDatos:
                    equipoId= dato.id_equipo_id #2
                    estadomou = dato.estado
                    
                    
                if equipoId == None:
                  

                
                
               
                    equiposTotales = Equipos.objects.all()
                        
                    
                        
                    sinEquipo = True
                    lista = zip(monitorDatos,equiposTotales)
                    return render(request, "Editar/editarTeclado.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "monitorRecibido":monitorRecibido,  "equiposTotales":equiposTotales, "sinEquipo":sinEquipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    equiposMon = Equipos.objects.filter(id_equipo = equipoId)
                    for eqE in equiposMon:
                        id_empleadoE = eqE.id_empleado_id 

                    empleadoDe = Empleados.objects.filter(id_empleado = id_empleadoE)
                

                    lista = zip(monitorDatos, equiposMon)
                    
                    equipos_totales = Equipos.objects.all()
                    arreglo_ids = []
                
                    for equi in equipos_totales:
                        arreglo_ids.append(equi.id_equipo)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == equipoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                    datos_equipo = []
                
                    
                    for id in arreglo_ids:
                        datos = Equipos.objects.filter(id_equipo = id)
                        for dato in datos:
                            id_equipo = dato.id_equipo
                            tipo = dato.tipo
                            marca = dato.marca
                            modelo = dato.modelo
                            foto = dato.imagen
                            id_empleado = dato.id_empleado_id
                        datos_equipo.append([id_equipo, tipo, marca,  modelo, foto])    

                        empleados = Empleados.objects.filter(id_empleado = id_empleado)
                       
                        

                  
                    return render(request, "Editar/editarMonitor.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "empleadoDe":empleadoDe, "equipos_totales":equipos_totales, "correo":correo, "lista":lista, "equiposMon":equiposMon, "empleados":empleados, "datos_equipo":datos_equipo, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    
        return render(request,"Editar/editarMonitor.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio  
    
def verTelefonos(request):
    
    if "idSesion" in request.session:

        estaEnVerTelefonos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        #arreglos telefonos en stock y activos
        telActivos = []
        telStock = []
        telActivosPrestados = []
        idsTelPrestados = []
        #obtener lista de todos los telefonos

        telefonosTotales = Telefonos.objects.all()
        telefonosPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Telefonos")
        for teP in telefonosPrestados:
            idTelP = teP.id_producto
            idsTelPrestados.append(idTelP)


        for tel in telefonosTotales:
            idTel = str(tel.id_telefono)
            if tel.id_empleado_id == None:
                ConPropietario = False
            else:
                ConPropietario = True
                idEmpl = str(tel.id_empleado_id)
            con = tel.conexion
            marcaT = tel.marca
            modeloT = tel.modelo
            estadoT = tel.estado
            fotoT = tel.foto
            extension = tel.extension
            nodo = tel.nodo
            activo = tel.activo

            if activo == "A":

                if ConPropietario == True:
                    encargado = Empleados.objects.filter(id_empleado = str(idEmpl))
                    for e in encargado:
                        idE = str(e.id_empleado)
                        nombres = e.nombre
                        apellidosE = e.apellidos
                        areaE = str(e.id_area_id)

                        encargadoNombre = idE + " " + nombres + " " + apellidosE 

                    areasT = Areas.objects.filter(id_area = areaE)
                    for a in areasT:
                        nombreA = a.nombre
                        color = a.color

                    areaEncargado = nombreA + " " + color

                   

                elif ConPropietario == False:
                    encargadoNombre = "Sin encargado"
                    nombreA = "Sin área"
                    color = ""
                    extension = "Sin extension"
                    nodo = "Sin nodo"

                telActivos.append([idTel,encargadoNombre, nombreA, color,   con, marcaT, modeloT, estadoT, fotoT, extension, nodo])

              

                if idTel in idsTelPrestados:
                    for telP in telefonosPrestados:
                        idTelPrestado = telP.id_producto
                        if idTel == idTelPrestado:
                            fecha = telP.fecha_prestamo
                            firma = telP.firma_entrega

                        telActivosPrestados.append([fecha, firma])
                else:
                    telActivosPrestados.append("Sin prestamo")

                

            if activo == "I":
                telStock.append([idTel, con, marcaT, modeloT, estadoT, fotoT])

            listaT = zip(telActivos, telActivosPrestados)






        return render(request, "Sistemas/Telefonos/verTelefonos.html", {"estaEnVerTelefonos":estaEnVerTelefonos, "ConPropietario":ConPropietario, "telActivos":telActivos,"telStock":telStock, "telActivosPrestados":telActivosPrestados, "listaT":listaT, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "telActivos":telActivos, "telStock":telStock})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def bajaTelefono(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idBaja= request.POST['idTelefonoBaja']
            
            datosTelefono = Telefonos.objects.filter(id_telefono = idBaja)
            
            
            for dato in datosTelefono:
                idTelefono = str(dato.id_telefono)
                marca = dato.marca
                modelo = dato.modelo
            
                
            

            
            nombreCompletoTelefono = marca + " " + modelo
           

            actualizacion = Telefonos.objects.filter(id_telefono = idTelefono).update(activo = "I", estado = "stockUsado", nodo = "", extension = "",id_empleado = "")

           
                    
            request.session['idTelefonoBaja'] = nombreCompletoTelefono
            prestamo =  PrestamosSistemas.objects.filter(id_producto = idBaja, tabla = "Telefonos")

            if prestamo:
                telefono = int(idBaja)
                borrado = PrestamosSistemas.objects.get(id_producto = telefono, tabla = "Telefonos")
                borrado.delete()
                    
            return redirect('/verTelefonos/')

                

               
                
                            
            
  
            
    else:
        return redirect('/login/') #redirecciona a url de inicio

def altaTelefono(request):

    if "idSesion" in request.session:
    
        id_empleado_admin = request.session['idSesion']
        if request.method == "POST":
        
            idAlta= request.POST['idTelefonoAlta']
            idsTelefonoP =[]
            datosTelefono = Telefonos.objects.filter(id_telefono = idAlta)
            
            for dato in datosTelefono:
                idTelefono = str(dato.id_telefono)
                marca = dato.marca
                modelo = dato.modelo
  
            nombreCompletoTelefono = marca + " " + modelo

            telefonosPrestados = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Telefonos")
            for dato in telefonosPrestados:
                idT = dato.id_producto
                idsTelefonoP.append(idT)

      

            
            actualizacion = Telefonos.objects.filter(id_telefono = idTelefono).update(activo = "A", estado = "activoFuncional")
            if actualizacion:
                            
                                
                            
                request.session['idTelefonoAlta'] = nombreCompletoTelefono
                                
                return redirect('/verTelefonos/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def agregarTelefonos(request):
    
    if "idSesion" in request.session:

        estaEnAgregarTelefonos = True
        registroTelefonoCompleto = False
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

     
        #Carga de todos los empleados para el select
        empleados = Empleados.objects.all()
        
        #Si se le dio clic al botón de Guardar tecldo
        if request.method == "POST":
            
           
            encargadoRecibido = request.POST['propietario']
            conexionRecibido = request.POST['conexion']
            marcaRecibido = request.POST['marcaTel']
            modeloRecibido = request.POST['modeloTel']
            estadoRecibido = request.POST['estadoTel']
            imagenRecibido = request.FILES.get('imagenTel')
            extensionRecibido = request.POST['extensiones']
            nodoRecibido = request.POST['nodo']

            if encargadoRecibido == "Sin encargado":
                if extensionRecibido == "Ninguna":
                    if nodoRecibido == "":
                        registroTelefono = Telefonos(conexion = conexionRecibido, marca = marcaRecibido, modelo = modeloRecibido, estado = estadoRecibido, foto = imagenRecibido,
                        nodo = "Sin nodo", activo = "I" )
                        registroTelefono.save()

            elif encargadoRecibido != "Sin encargado":
                registroTelefono = Telefonos(id_empleado = Empleados.objects.get(id_empleado = encargadoRecibido), conexion = conexionRecibido, marca = marcaRecibido, modelo = modeloRecibido,
                estado= estadoRecibido, foto = imagenRecibido, extension = extensionRecibido, nodo = nodoRecibido, activo = "A")
                registroTelefono.save()

            if registroTelefono:
                registroTelefonoCompleto = True
                texto  = "Se ha registrado el teléfono "+ marcaRecibido + " " + modeloRecibido
                
            return render(request, "Sistemas/Telefonos/agregarTelefonos.html", {"estaEnAgregarTelefonos":estaEnAgregarTelefonos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, 
                                                                          "registroTelefonoCompleto":registroTelefonoCompleto, "texto":texto})



        return render(request, "Sistemas/Telefonos/agregarTelefonos.html", {"estaEnAgregarTelefonos":estaEnAgregarTelefonos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
         "empleados":empleados, "registroTelefonoCompleto":registroTelefonoCompleto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

  
def editarTelefono(request):
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            telefonoRecibido = request.POST['idTelefonoEditar']
            telefonoDatos = Telefonos.objects.filter(id_telefono=telefonoRecibido)

           
            for dato in telefonoDatos:
                empleadoId= dato.id_empleado_id #2
                extensionTel = dato.extension
           

            empleadosTel = Empleados.objects.filter(id_empleado= empleadoId)
       
              
               
                
            if empleadoId == None:
                extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                for ex in extension:
                    if ex == extensionTel:
                        extension.remove(ex)


                empleadosTotales = Empleados.objects.all()
 
                    
                sinEmpleado = True
                lista = zip(telefonoDatos,empleadosTotales)
                return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "empleadosTel":empleadosTel, "extension":extension, "lista":lista, "telefonoRecibido":telefonoRecibido, "empleadosTotales":empleadosTotales, "sinEmpleado":sinEmpleado, 
                                                                    "cartuchosNoti":cartuchosNoti, "mantenimientosNoti":mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                
                empleadosTel = Empleados.objects.filter(id_empleado = empleadoId)
                extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                for ex in extension:
                    if ex == extensionTel:
                        extension.remove(ex)

                for eqE in empleadosTel:
                        id_area = eqE.id_area_id 

                areaDe = Areas.objects.filter(id_area = id_area)
     
                
                lista = zip(telefonoDatos,empleadosTel)
                
                empleados_totales = Empleados.objects.all()
                arreglo_ids = []
                
                for equi in empleados_totales:
                    arreglo_ids.append(equi.id_empleado)
                    
                    #[1,2,3]
                    
                for id in arreglo_ids:
                     if id == empleadoId: #si 2 == 2
                        arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                 
                datos_empleados = []
                    
                for id in arreglo_ids:
                    datos = Empleados.objects.filter(id_empleado = id)
                    for dato in datos:
                        id_empleados = dato.id_empleado
                        nombres = dato.nombre
                        apellido = dato.apellidos
                        foto = dato.imagen_empleado
                         
                           
                    datos_empleados.append([id_empleados, nombres, apellido, foto])    

                        
                
            
            return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "extension":extension, "correo":correo, "lista":lista, "empleadosTel":empleadosTel, "empleados_totales":empleados_totales, "areaDe":areaDe, "datos_empleados":datos_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

        return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def editarTelefonoBd(request):
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            telefonoId = request.POST['idTelefono']
            empleado_actualizar = request.POST['propietario']
            estado_actualizar = request.POST['estado']
            nodo_actualizar = request.POST['nodo']
            extension_actualizar = request.POST['extension']
         

            
            if empleado_actualizar == "sinEmpleado":
                actualizar = Telefonos.objects.filter(id_telefono=telefonoId).update( id_empleado_id=None,estado= estado_actualizar, activo="I", nodo = nodo_actualizar, extension = extension_actualizar)
                
                
            elif empleado_actualizar !=  "sinEmpleado": 
                int_empleado = int(empleado_actualizar)
                actualizar = Telefonos.objects.filter(id_telefono=telefonoId).update( id_empleado_id=Empleados.objects.get(id_empleado = int_empleado),
                                                 estado= estado_actualizar, activo="A", nodo = nodo_actualizar, extension = extension_actualizar)
            
            if actualizar:
               
                datos = Telefonos.objects.filter(id_telefono = telefonoId)
            

                
                for dato in datos:
               
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoTelefono = marca + " " + modelo
                
                
                
                editado = True
                textoEdicion = "Se ha editado al teléfono " + todoTelefono + " con éxito!"
              
                
               
                

                telefonoRecibido = telefonoId
                telefonoDatos = Telefonos.objects.filter(id_telefono=telefonoRecibido)

                
                for dato in telefonoDatos:
                    empleadoId= dato.id_empleado_id #2
                    extensionTel = dato.extension
                    
                if empleadoId == None:
                    extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                    for ex in extension:
                        if ex == extensionTel:
                            extension.remove(ex)
                        

                    empleadosTotales = Empleados.objects.all()
                            
               
                    
                        
                    sinEmpleado = True
                    lista = zip(telefonoDatos,empleadosTotales)

                    prestamo =  PrestamosSistemas.objects.filter(id_producto = telefonoId)

                    if prestamo:
                        telefono = int(telefonoId)
                        borrado = PrestamosSistemas.objects.get(id_producto = telefono, tabla = "Telefonos")
                        borrado.delete()
                            
                        return redirect('/verTelefonos/')


                    return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,"extension":extension, "lista": lista, "telefonoRecibido":telefonoRecibido, "equiposTotales":equiposTotales, "sinEmpleado":sinEmpleado, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    empleadosTel = Empleados.objects.filter(id_empleado = empleadoId)
                    extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                    for ex in extension:
                        if ex == extensionTel:
                            extension.remove(ex)

                    for eqE in empleadosTel:
                        id_area = eqE.id_area_id 

                    areaDe = Areas.objects.filter(id_area = id_area)
                  


                    lista = zip(telefonoDatos, empleadosTel)
                    
                    empleados_totales = Empleados.objects.all()
                    arreglo_ids = []
                
                    for equi in empleados_totales:
                        arreglo_ids.append(equi.id_empleado)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == empleadoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                 
                    datos_empleados = []
                    
                    for id in arreglo_ids:
                        datos = Empleados.objects.filter(id_empleado = id)
                        for dato in datos:
                            id_empleados = dato.id_empleado
                            nombres = dato.nombre
                            apellido = dato.apellidos
                            foto = dato.imagen_empleado
                         
                           
                        datos_empleados.append([id_empleados, nombres, apellido, foto])    

                 
                       
                       

                  
                    return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "areaDe":areaDe, "extension":extension, "empleados_totales":empleados_totales, "correo":correo, "lista":lista, "empleadosTel":empleadosTel, "datos_empleados":datos_empleados, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
            else:
                datos = Telefonos.objects.filter(id_telefono = telefonoId)

                
                for dato in datos:
                 
                    marca = dato.marca
                    modelo = dato.modelo
                    
                todoTelefono = marca + " " + modelo
                
                
                editado = True
                textoEdicion = "Error en la base de datos!"
               
             
                telefonoRecibido = telefonoId
                telefonoDatos = Telefonos.objects.filter(id_telefono=telefonoRecibido)

                
                for dato in telefonoDatos:
                    empleadoId= dato.id_empleado_id #2
                    extensionTel = dato.extension
                    
                    
                if empleadoId == None:
                    extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                    for ex in extension:
                        if ex == extensionTel:
                            extension.remove(ex)
                  

                
                
               
                    empleadosTotales = Empleados.objects.all()
                        
                    
                        
                    sinEmpleado = True
                    lista = zip(telefonoDatos,empleadosTotales)
                    return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto,"extension":extension, "correo":correo, "lista":lista, "telefonoRecibido":telefonoRecibido,  "empleadosTotales":empleadosTotales, "sinEmpleado":sinEmpleado, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    
                    empleadosTel = Empleados.objects.filter(id_empleado = empleadoId)
                    extension = ["Ninguna", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118","119","120"]
                    for ex in extension:
                        if ex == extensionTel:
                            extension.remove(ex)

                    for eqE in empleadosTel:
                        id_area = eqE.id_area_id 

                    areaDe = Areas.objects.filter(id_area = id_area)
                  


                    lista = zip(telefonoDatos, empleadosTel)
                    
                    empleados_totales = Empleados.objects.all()
                    arreglo_ids = []
                
                    for equi in empleados_totales:
                        arreglo_ids.append(equi.id_empleado)
                    
                    #[1,2,3]
                    
                    for id in arreglo_ids:
                        if id == empleadoId: #si 2 == 2
                            arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                 
                    datos_empleados = []
                    
                    for id in arreglo_ids:
                        datos = Empleados.objects.filter(id_empleado = id)
                        for dato in datos:
                            id_empleados = dato.id_empleado
                            nombres = dato.nombre
                            apellido = dato.apellidos
                            foto = dato.imagen_empleado
                         
                           
                        datos_empleados.append([id_empleados, nombres, apellido, foto])    
                       
                        

                  
                    return render(request, "Editar/editarTelefono.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "extension":extension,"areaDe":areaDe, "empleados_totales":empleados_totales, "correo":correo, "lista":lista, "empleadosTel":empleadosTel, "datos_empleados":datos_empleados, 
                                                                        "editado":editado, "textoEdicion":textoEdicion, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    
        return render(request,"Editar/editarTelefono.html", {"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio  
    
def extensionesTel(request):
    
    if "idSesion" in request.session:

        estaEnExtensionesTelefonos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

         #arreglos telefonos en stock y activos
        telActivos = []
        areasT=[]
        encargado = []
       
        #obtener lista de todos los telefonos

        telefonosTotales = Telefonos.objects.all()
        for tel in telefonosTotales:
            idTel = str(tel.id_telefono)
            idEmpl = str(tel.id_empleado_id)
            con = tel.conexion
            marcaT = tel.marca
            modeloT = tel.modelo
            estadoT = tel.estado
            fotoT = tel.foto
            extension = tel.extension
            nodo = tel.nodo
            activo = tel.activo

            if activo == "A":
                encargado = Empleados.objects.filter(id_empleado = str(idEmpl))
                for e in encargado:
                    idE = str(e.id_empleado)
                    nombres = e.nombre
                    apellidosE = e.apellidos
                    areaE = str(e.id_area_id)
                    puestoE = e.puesto
                    encargadoNombre = nombres + " " + apellidosE 
                areasT = Areas.objects.filter(id_area = areaE)
                for areaTelefono in areasT:
                    nombreA = areaTelefono.nombre
                    colorA = areaTelefono.color


                    
                telActivos.append([idTel,encargadoNombre,  nombreA, colorA, extension])

                
             

                

            



        return render(request, "Sistemas/Telefonos/extensiones.html", {"estaEnExtensionesTelefonos":estaEnExtensionesTelefonos,"telActivos":telActivos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
def agregarDiscosDuros(request):
        
    if "idSesion" in request.session:
    
        estaEnAgregarDiscosDuros = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        #empleados en select
        empleados = Empleados.objects.all()
        #Si se le dio clic al botón de Guardar tecldo
        if request.method == "POST":
            
           
            tipoRecibido = request.POST['tipoDisco']
            marcaRecibido = request.POST['marcasDisco']
            almacenamientoRecibido = request.POST['capacidadAlm']
            estadoRecibido = request.POST['estadoDisco']
            dimensionRecibido = request.POST['dimensiones']
            usoRecibido = request.POST['almacenamientoUso']
            numrespaldosRecibido = request.POST['numeroEmpleadosRespaldo']
            
            empleado = "empleado"
            fecha = "fecha_respaldo"
            if usoRecibido != "":
                almLibre = int(almacenamientoRecibido) - int(usoRecibido)
           
            idEmpleado = 0
            listaEmpleados=[]
            idsEmpleados =[]
            fechas = []
           
            
            
            
           

            if numrespaldosRecibido == "":
                if usoRecibido == "":
                    #registro disco
                    registroDisco = DiscosDuros(tipo = tipoRecibido, marca = marcaRecibido, capacidad = almacenamientoRecibido, dimension = dimensionRecibido, estado = estadoRecibido
                ,  alm_libre = almacenamientoRecibido)
                    registroDisco.save()
                else:
                    #registro disco
                    registroDisco = DiscosDuros(tipo = tipoRecibido, marca = marcaRecibido, capacidad = almacenamientoRecibido, dimension = dimensionRecibido, alm_uso = usoRecibido, estado = estadoRecibido,
                    alm_libre = almLibre)
                    registroDisco.save()

            
            elif numrespaldosRecibido != "":
                for empleadosRes in range(int(numrespaldosRecibido)):
                    idEmpleado= idEmpleado + 1
                
                    nameEmpleado = "empleado" + str(idEmpleado)
                    nameFecha = "fecha_respaldo" + str(idEmpleado)
                    
                    textoNombreEmpleado = request.POST[nameEmpleado]
                    fechaRecibido = request.POST[nameFecha]
                    fechas.append(fechaRecibido)
                    idsEmpleados.append(textoNombreEmpleado)
                  

                lista = zip(idsEmpleados, fechas)
                #registro disco
                registroDisco = DiscosDuros(tipo = tipoRecibido, marca = marcaRecibido, capacidad = almacenamientoRecibido, dimension = dimensionRecibido, alm_uso = usoRecibido, estado = estadoRecibido,
                alm_libre = almLibre)
                registroDisco.save()
                if registroDisco:
                    registrarDiscoID = DiscosDuros.objects.count()
                    for empleadod, fecha in lista:
                        registroEmpleadoDisco = EmpleadosDiscosDuros(id_empleado = Empleados.objects.get(id_empleado= empleadod), id_disco = DiscosDuros.objects.get(id_disco=registrarDiscoID), fecha = fecha)
                        registroEmpleadoDisco.save()
            

            
            discoGuardado = True
            discoGuardadoTexto = "El disco duro" + tipoRecibido + " " + marcaRecibido + " fue guardado con éxito!"

            
            return render(request, "discosDuros/agregarDiscosDuros.html", {"estaEnAgregarDiscosDuros":estaEnAgregarDiscosDuros,"id_admin":id_admin, "discoGuardado":discoGuardado, "discoGuardadoTexto":discoGuardadoTexto,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
                "empleados": empleados})


        return render(request, "discosDuros/agregarDiscosDuros.html", {"estaEnAgregarDiscosDuros":estaEnAgregarDiscosDuros,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "empleados": empleados})
    else:
        return redirect ('/login/')

def verDiscosDuros(request):
    
    if "idSesion" in request.session:
        
        estaEnVerDiscosDuros = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        

      
        discosSiRespaldos = []
        discosEnPrestamos = []
        idsDiscosPrestamos = []


        #lista de todos los discos duros
        totaldiscos = DiscosDuros.objects.all()
        discosPrestados = PrestamosSistemas.objects.filter(devolucion = "S", tabla = "DiscosDuros")
        conPrestamo = True
        for disP in discosPrestados:
            iD = disP.id_producto
            fechad = disP.fecha_prestamo
            idsDiscosPrestamos.append(iD)
            if disP.id_empleado_id == None:
                conPrestamo = False
                                
            else:
                conPrestamo = True
                idEmpleadoP = disP.id_empleado_id
              

        
       
        for disco in totaldiscos:
            idDisco = int(disco.id_disco)

                

            discosRespaldos = EmpleadosDiscosDuros.objects.filter(id_disco_id = idDisco)
            discosSiPrestados = PrestamosSistemas.objects.filter(devolucion = "S", tabla = "DiscosDuros", id_producto = idDisco)

            if discosRespaldos:
                empleadosEnDisco = []
                fechasDisco = []
                datosEmpleado = ""
                for respa in discosRespaldos:
                    
                    
                    empleados = respa.id_empleado_id
                    fecha = respa.fecha

                    datosEmpleadosRespaldos = Empleados.objects.filter(id_empleado = empleados)

                    for empleado in datosEmpleadosRespaldos:
                        ids = str (empleado.id_empleado)
                        nombres = empleado.nombre
                        apellido = empleado.apellidos

                        datosEmpleado = ids + " " + nombres + " " + apellido 
                    empleadosEnDisco.append(datosEmpleado)
                    fechasDisco.append(fecha)
                discosSiRespaldos.append([empleadosEnDisco,fechasDisco])


            else:
                discosSiRespaldos.append("n")

            if discosSiPrestados:
                for dis in discosSiPrestados:
                    idd = dis.id_producto
                    if dis == idd:
                        fechad = dis.fecha_prestamo
                        idEmpleadoP = dis.id_empleado_id
                            
                    empleadoDatos = Empleados.objects.filter(id_empleado = idEmpleadoP)
                    for eD in empleadoDatos:
                        nombreD = eD.nombre
                        apellidoD = eD.apellidos
                    empleadoPrestamo = nombreD + " " + apellidoD
                            

                discosEnPrestamos.append([empleadoPrestamo, fechad])

            else:
                
                discosEnPrestamos.append("Sin prestamo")

              
                
        
            
                    
        lista = zip(totaldiscos, discosSiRespaldos, discosEnPrestamos)    

        if "idDiscoActualizado" in request.session:
            discoActualizado=True
            textoActualizado= request.session['idDiscoActualizado']
            del request.session["idDiscoActualizado"] 

            return render(request, "discosDuros/verDiscosDuros.html", {"estaEnVerDiscosDuros":estaEnVerDiscosDuros, "discoActualizado":discoActualizado,"textoActualizado":textoActualizado, "id_admin":id_admin, "conPrestamo":conPrestamo, "discosEnPrestamos":discosEnPrestamos, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "lista":lista})     


        return render(request, "discosDuros/verDiscosDuros.html", {"estaEnVerDiscosDuros":estaEnVerDiscosDuros, "id_admin":id_admin, "conPrestamo":conPrestamo, "discosEnPrestamos":discosEnPrestamos, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "lista":lista})
    else:
    
        return redirect ('/login/')

def editarDisco(request):
    if "idSesion" in request.session:
        
        estaEnCartasBitacora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
           
            discoRecibido = request.POST['idDiscoEditar']
            discoDatos = DiscosDuros.objects.filter(id_disco=discoRecibido)
            sinPrestamo = True
            DiscosenPrestamos = PrestamosSistemas.objects.filter(devolucion = "S", tabla = "DiscosDuros", id_producto = discoRecibido)
            empleadosTotales = Empleados.objects.filter(activo = "A")
            for disP in DiscosenPrestamos:
                
               
                if disP.id_empleado_id == None:
                    sinPrestamo = True
                else:
                    sinPrestamo = False
                    idEmpleadoP = disP.id_empleado_id


                #verificar si tiene respaldos 
            respaldosDisco = EmpleadosDiscosDuros.objects.filter(id_disco = discoRecibido)
            idsEmpleadosRespaldo = []
            idsEmpleadosRespaldos2 = []
            if respaldosDisco:
                discoTieneRespaldo = True
                for respaldo in respaldosDisco:
                    idFila = respaldo.id
                    idEmpleadoRespaldo = respaldo.id_empleado_id
                    fechaRespaldo = respaldo.fecha
                    datosEmpleados = Empleados.objects.filter(id_empleado = idEmpleadoRespaldo)
                    for dato in datosEmpleados:
                        nombreER = dato.nombre
                        apellidoER = dato.apellidos

                    idsEmpleadosRespaldo.append([idEmpleadoRespaldo, nombreER, apellidoER, fechaRespaldo, idFila])
                    idsEmpleadosRespaldos2.append(idEmpleadoRespaldo)
            else:
                discoTieneRespaldo = False

         
            if sinPrestamo == False:
                
                empleadosDisco = Empleados.objects.filter(id_empleado = idEmpleadoP)
                

                for eqE in empleadosDisco:
                        id_area = eqE.id_area_id 

                areaDe = Areas.objects.filter(id_area = id_area)
     
                
                lista = zip(discoDatos,empleadosDisco)
                
                empleados_totales = Empleados.objects.all()
                arreglo_ids = []
                
                for equi in empleados_totales:
                    arreglo_ids.append(equi.id_empleado)
                    
                    #[1,2,3]
                    
                for id in arreglo_ids:
                     if id == idEmpleadoP: #si 2 == 2
                        arreglo_ids.remove(id)
                            
                    #[1,3]
                    
                 
                datos_empleados = []
                    
                for id in arreglo_ids:
                    datos = Empleados.objects.filter(id_empleado = id)
                    for dato in datos:
                        id_empleados = dato.id_empleado
                        nombres = dato.nombre
                        apellido = dato.apellidos
                        foto = dato.imagen_empleado
                         
                           
                    datos_empleados.append([id_empleados, nombres, apellido, foto])
                    

                if discoTieneRespaldo == True:

                    return render(request, "Editar/editarDiscoDuro.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "empleadosTotales":empleadosTotales,"discoDatos":discoDatos, "discoTieneRespaldo":discoTieneRespaldo, "idsEmpleadosRespaldo":idsEmpleadosRespaldo, "idsEmpleadosRespaldos2":idsEmpleadosRespaldos2, "correo":correo, "lista":lista, "empleadosDisco":empleadosDisco, "empleados_totales":empleados_totales, "areaDe":areaDe, "datos_empleados":datos_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    return render(request, "Editar/editarDiscoDuro.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto,"empleadosTotales":empleadosTotales,"discoDatos":discoDatos, "discoTieneRespaldo":discoTieneRespaldo, "correo":correo, "lista":lista, "empleadosDisco":empleadosDisco, "empleados_totales":empleados_totales, "areaDe":areaDe, "datos_empleados":datos_empleados, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})

                            
                        
            else:

                if discoTieneRespaldo == True:


                    return render(request, "Editar/editarDiscoDuro.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto,"discoDatos":discoDatos,"empleadosTotales":empleadosTotales,"discoTieneRespaldo":discoTieneRespaldo, "idsEmpleadosRespaldo":idsEmpleadosRespaldo, "idsEmpleadosRespaldos2":idsEmpleadosRespaldos2, "correo":correo, "discoRecibido":discoRecibido, "sinPrestamo":sinPrestamo, 
                                                                        "cartuchosNoti":cartuchosNoti, "mantenimientosNoti":mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                else:
                    return render(request, "Editar/editarDiscoDuro.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto,"discoDatos":discoDatos,"empleadosTotales":empleadosTotales,"discoTieneRespaldo":discoTieneRespaldo,"correo":correo, "discoRecibido":discoRecibido, "sinPrestamo":sinPrestamo, 
                                                                        "cartuchosNoti":cartuchosNoti, "mantenimientosNoti":mantenimientosNoti,"discoTieneRespaldo":discoTieneRespaldo, "numeroNoti":numeroNoti, "foto":foto})
                
                    

                        
                
            
            

        return render(request, "Editar/editarDiscoDuro.html", {"id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def editarDiscoBd(request):
    if "idSesion" in request.session:
        
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            discoId = request.POST['idDisco']
            
            estado_actualizar = request.POST['estado']
            almacenamientoUso_actualizar = request.POST['almacenamientoUso']
            numrespaldosRecibido = request.POST['numeroEmpleadosRespaldo']

            discoDatos = DiscosDuros.objects.filter(id_disco = discoId)
            for datoD in discoDatos:
                capAlamacenamiento = datoD.capacidad

            

            empleado = "empleado"
            fecha = "fecha_respaldo"
            if almacenamientoUso_actualizar != "":
                almLibre = int(capAlamacenamiento) - int(almacenamientoUso_actualizar)
           
            idEmpleado = 0
            listaEmpleados=[]
            idsEmpleados =[]
            fechas = []
           
            
            
            
           

            if numrespaldosRecibido == "":
                if almacenamientoUso_actualizar == "":
                   
                    actualizar = DiscosDuros.objects.filter(id_disco = discoId).update(estado = estado_actualizar)
            
                else:
                    #registro disco
                    actualizar = DiscosDuros.objects.filter(id_disco = discoId).update(estado = estado_actualizar, alm_libre = almLibre, alm_uso= almacenamientoUso_actualizar)

              
                respaldosTotales = EmpleadosDiscosDuros.objects.filter(id_disco_id = discoId)

                nombresInputs = []
                
                for respaldo in respaldosTotales:
                    idRespaldo = respaldo.id
                    nameInput = "respaldo" + str(idRespaldo)
                    #Condicion para si se mando un nameinput igual, sin validar que sea chequeado o no.. 
                    #Si se mando algo...
                    
                    if request.POST.get(nameInput):
                        jhjjh=True
                    else:
                        registroBorrar = EmpleadosDiscosDuros.objects.get(id = idRespaldo)
                        registroBorrar.delete()

                   
                     
                    
                            
                          

                    

            
            elif numrespaldosRecibido != "":

                
                respaldosTotales = EmpleadosDiscosDuros.objects.filter(id_disco_id = discoId)

                nombresInputs = []
                
                for respaldo in respaldosTotales:
                    idRespaldo = respaldo.id
                    nameInput = "respaldo" + str(idRespaldo)
                    #Condicion para si se mando un nameinput igual, sin validar que sea chequeado o no.. 
                    #Si se mando algo...
                    
                    if request.POST.get(nameInput):
                        jhjjh=True
                    else:
                        registroBorrar = EmpleadosDiscosDuros.objects.get(id = idRespaldo)
                        registroBorrar.delete()

                
               
                


                for empleadosRes in range(int(numrespaldosRecibido)):
                    idEmpleado= idEmpleado + 1
                
                    nameEmpleado = empleado + str(idEmpleado)
                    nameFecha = fecha + str(idEmpleado)
                    
                    textoNombreEmpleado = request.POST[nameEmpleado]
                    fechaRecibido = request.POST[nameFecha]
                    fechas.append(fechaRecibido)
                    idsEmpleados.append(textoNombreEmpleado)
                    
                lista1 = zip(idsEmpleados, fechas)

           
                    
                    
                        
                for empleadod, fecha in lista1:
                    registroEmpleadoDisco = EmpleadosDiscosDuros(id_empleado = Empleados.objects.get(id_empleado= empleadod), id_disco = DiscosDuros.objects.get(id_disco=discoId), fecha = fecha)
                    registroEmpleadoDisco.save()

                if registroEmpleadoDisco:
                    

                    actualizar = DiscosDuros.objects.filter(id_disco = discoId).update(estado = estado_actualizar, alm_libre = almLibre, alm_uso= almacenamientoUso_actualizar)

               
            
      
            
            if actualizar:
                
               
                datos = DiscosDuros.objects.filter(id_disco = discoId)
            

                
                for dato in datos:
                    tipo = dato.tipo
                    marca = dato.marca
                    dimension = dato.dimension
                    
                todoDisco = tipo + " " + marca + " " + dimension
                
                
                
                editado = True
                textoEdicion = "Se ha editado al disco " + todoDisco + " con éxito!"

                discoRecibido = discoId
                discoDatos = DiscosDuros.objects.filter(id_disco=discoRecibido)

                  
                
              
                
               
   
                
            else:
                datos = DiscosDuros.objects.filter(id_disco = discoId)

                
                for dato in datos:
                    tipo = dato.tipo
                    marca = dato.marca
                    dimension = dato.dimension
                    
                todoDisco = tipo + " " + marca + " " + dimension
                
                
                editado = True
                textoEdicion = "Error en la base de datos!"
                discoRecibido = discoId
                discoDatos = DiscosDuros.objects.filter(id_disco=discoRecibido)
            texto = ""
            for name in nombresInputs:     
                texto += name + " "
            request.session['idDiscoActualizado'] = textoEdicion
            
            return redirect('/verDiscosDuros/')
               
             
        

                    


            
                
    
        return render(request,"Editar/editarDiscoDuro.html", {"id_admin":id_admin, "nombresInputs":nombresInputs, "nombreCompleto":nombreCompleto,"discoDatos":discoDatos, "discoRecibido":discoRecibido, "editado":editado,"textoEdicion":textoEdicion, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio   

def agregarUSB(request):
        
    if "idSesion" in request.session:
    
        estaEnAgregarUSB= True
        guardadoUSB = False
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        if request.method == "POST":
            marcaRecibido = request.POST['marca']
            modeloRecibido = request.POST['modelo']
            capaRecibido = int (request.POST['capacidad'])
            cantRecibido = int (request.POST['cantidad'])

            if modeloRecibido == "":
                registroUSB = MemoriasUSB(marca = marcaRecibido , capacidad = capaRecibido, cantidadStock = cantRecibido)
                registroUSB.save()
            else:
                registroUSB = MemoriasUSB(marca = marcaRecibido , modelo = modeloRecibido, capacidad = capaRecibido, cantidadStock = cantRecibido)
                registroUSB.save()

            if registroUSB:
                guardadoUSB = True 
                texto = "La memoria USB " + " " + marcaRecibido + " " + modeloRecibido + " se agregó con éxito!"
            
            return render(request, "memoriasUSB/agregarUSB.html", {"estaEnAgregarUSB":estaEnAgregarUSB,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "guardadoUSB": guardadoUSB, "texto": texto})
            



        return render(request, "memoriasUSB/agregarUSB.html", {"estaEnAgregarUSB":estaEnAgregarUSB,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "guardadoUSB": guardadoUSB})
    else:
        return redirect ('/login/')

def verUSB(request):
    
    if "idSesion" in request.session:
        
        estaEnVerUSB = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        memorias = MemoriasUSB.objects.all()

        if "idUsbActualizado" in request.session:
            usbActualizado=True
            textoActualizado= request.session['idUsbActualizado']
            del request.session["idUsbActualizado"]
            
            return render(request, "memoriasUSB/verUSB.html", {"estaEnVerUSB":estaEnVerUSB,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "memorias": memorias, "usbActualizado":usbActualizado, "textoActualizado":textoActualizado})    



        return render(request, "memoriasUSB/verUSB.html", {"estaEnVerUSB":estaEnVerUSB,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "memorias": memorias})
    else:
    
        return redirect ('/login/')


def actualizarUSB(request):
    
    if "idSesion" in request.session:
    
        Insumos = True
        estaEnVerInsumos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        
        if request.method == "POST":
            
            id_usb_recibido = request.POST['idUsb']
            cantida_recibida = request.POST['cantidadUsb']
            
            datosUSB = MemoriasUSB.objects.filter(id_usb=id_usb_recibido)
            
            for dato in datosUSB:
                marca = dato.marca
                modelo = dato.modelo
                
                
    
            
            actualizar = MemoriasUSB.objects.filter(id_usb=id_usb_recibido).update(cantidadStock=cantida_recibida)
            
            if actualizar:
                if modelo != "":
                
                    textoUSB = "Se ha actualizado el stock de la memoria USB  "+ marca+" "+ modelo  + " con éxito!"
                        
                    request.session['idUsbActualizado'] = textoUSB
                else: 
                    textoUSB = "Se ha actualizado el stock de la memoria USB  "+ marca + " con éxito!"
                        
                    request.session['idUsbActualizado'] = textoUSB
            
            return redirect('/verUSB/')
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
def agregarPrestamos(request):
        
    if "idSesion" in request.session:
    
        estaEnAgregarPrestamo= True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Empleados para select de empleados
        empleados = Empleados.objects.filter(activo = "A", correo__icontains = "@customco.com.mx")
        
        #Impresoras para select de impresoras
        impresoras = Impresoras.objects.all()
        
        #Computadoras para select de computadoras
        query = Q(estado='Funcional')
        query.add(Q(estado='Reparación'), Q.OR)
        query.add(Q(activo='I'), Q.AND)
        computadoras = Equipos.objects.filter(query)
        
        #Discos Duros.
        discosDuros = DiscosDuros.objects.all()
        
        #Monitores
        monitores = Monitores.objects.all() #Inactivos solamente
        
        #Teclados
        teclados = Teclados.objects.all() #Inactivos solamente
        
        #Mouses
        mouses = Mouses.objects.filter(activo = "I") #Inactivos solamente
        
        #Teléfonos
        telefonos = Telefonos.objects.all()#Inactivos solamente
        
        #USB
        memoriasUsb = MemoriasUSB.objects.all()

        fecha = datetime.now()
        
        #Clic en botón Realizar préstamo.
        if request.method == "POST":
            estatus = ""
            empleadoSolicitante = request.POST['solicitante']
            tabla = request.POST['clasificacion']
            
            if tabla == "otro":
                equipoAPrestar = ""
                otro = request.POST['otroEquipo']
            else:
                otro = ""
                equipoAPrestar = ""
                
                if tabla == "Impresoras":
                    equipoAPrestar = request.POST['impresora']
                elif tabla == "Equipos":
                    equipoAPrestar = request.POST['equipo']
                elif tabla == "DiscosDuros":
                    equipoAPrestar = request.POST['discoduro']
                elif tabla == "Monitores":
                    equipoAPrestar = request.POST['monitor']
                elif tabla == "Teclados":
                    equipoAPrestar = request.POST['teclado']
                elif tabla == "Mouses":
                    equipoAPrestar = request.POST['mouse']
                elif tabla == "Telefonos":
                    equipoAPrestar = request.POST['telefono']
                elif tabla == "MemoriasUSB":
                    equipoAPrestar = request.POST['usb']
                    
            cantidad = request.POST['cantidad']
            fecha_prestamo = request.POST['fecha']
            fecha_separada = fecha_prestamo.split("/") #29   06    2018            2018     29   06
            fecha_normal = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
            canvasLargo = request.POST['canvasData']
            format, imgstr = canvasLargo.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= str(empleadoSolicitante) + '.' + ext)
            condiciones = request.POST['condiciones']

            if request.POST.get('devolucion', False): #Checkeado
                devolucion = "S"
            elif request.POST.get('devolucion', True): #No checkeado
                devolucion = "N"
            
            if devolucion == "S":
                estatus = "Prestamo"
            elif devolucion == "N":
                estatus = "Finalizado"

            registroPrestamo = PrestamosSistemas(id_empleado = Empleados.objects.get(id_empleado = empleadoSolicitante), tabla = tabla, id_producto = equipoAPrestar, otro = otro, cantidad = cantidad, fecha_prestamo = fecha_normal,
            firma_entrega = archivo ,devolucion = devolucion, condiciones = condiciones, estatus = estatus)

            registroPrestamo.save()

            if registroPrestamo:
                prestamo = True
                texto ="El prestamo ha sido creado satisfactoriamente"
            
            return render(request, "prestamos/agregarPrestamo.html", {"estaEnAgregarPrestamo":estaEnAgregarPrestamo,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
            "empleados": empleados, "impresoras":impresoras, "computadoras":computadoras, "discosDuros":discosDuros, 
            "monitores":monitores, "teclados":teclados, "mouses":mouses, "telefonos":telefonos, "memoriasUsb":memoriasUsb, "prestamo": prestamo, "texto": texto, "fecha":fecha})
            
            
            
                
                
                    
        
    
        return render(request, "prestamos/agregarPrestamo.html", {"estaEnAgregarPrestamo":estaEnAgregarPrestamo,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "empleados": empleados, "impresoras":impresoras, "computadoras":computadoras, "discosDuros":discosDuros, 
        "monitores":monitores, "teclados":teclados, "mouses":mouses, "telefonos":telefonos, "memoriasUsb":memoriasUsb, "fecha":fecha})
    else:
        return redirect ('/login/')

def verPrestamos(request):

    if "idSesion" in request.session:
        
        estaEnVerPrestamos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

        prestamosNOaplicaDev = PrestamosSistemas.objects.filter(devolucion__icontains = "N")
        prestamosSINdevolver = PrestamosSistemas.objects.filter(devolucion__icontains = "S", estatus__icontains = "Prestamo")
        prestamosSIdevolvueltos = PrestamosSistemas.objects.filter(devolucion__icontains = "S", estatus__icontains = "Finalizado")
        

        
        #prestamos no aplica devolucion
        
        empleadosNoAplica = []
        datosCompletosEmpleadosNoAplica = []
        equipoPrestadoClasificacion = []
        fotosEquipos = []
        
    
        
        for prestamos in prestamosNOaplicaDev:
                
            empleadosNoAplica.append(prestamos.id_empleado_id)

            if prestamos.tabla == "otro":
                
                equipoPrestadoClasificacion.append(prestamos.otro)
            
            elif prestamos.tabla != "otro":
                equipo = prestamos.id_producto

                if prestamos.tabla == "Impresoras":
                    
                    datosImpresora= Impresoras.objects.filter(id_impresora = equipo)
                    for dato in datosImpresora:
                        marcaI = dato.marca
                        modeloI = dato.modelo
                        fotoI = dato.imagen
                        impresora = marcaI + " " + modeloI
                    equipoPrestadoClasificacion.append("Impresora " + impresora)
                    fotosEquipos.append(fotoI)
                
                elif prestamos.tabla  == "Equipos":
                    datosEquipo= Equipos.objects.filter(id_equipo = equipo)
                    for datos in datosEquipo:
                        tipoE = datos.tipo
                        marcaE = datos.marca
                        modeloE = datos.modelo
                        fotoE = datos.imagen
                        equipoC = tipoE + " " + marcaE + " " + modeloE
                    equipoPrestadoClasificacion.append("Equipo " + equipoC)
                    fotosEquipos.append(fotoE)
                    
                elif prestamos.tabla  == "DiscosDuros":
                    datosDiscos= DiscosDuros.objects.filter(id_disco = equipo)
                    for datoD in datosDiscos:
                        tipoD = datoD.tipo
                        marcaD = datoD.marca
                        fotoD = "Sin foto"
                       
                        disco = tipoD + " " + marcaD
                    equipoPrestadoClasificacion.append("Disco Duro " + disco)
                    fotosEquipos.append(fotoD)
                  
                elif prestamos.tabla  == "Monitores":
                    datosMonitor= Monitores.objects.filter(id_monitor = equipo)
                    for datoM in datosMonitor:
                        marcaM = datoM.marca
                        modeloM = datoM.modelo
                        fotoM = datoM.foto
                       
                        monitor = marcaM + " " + modeloM
                    equipoPrestadoClasificacion.append("Monitor " + monitor)
                    fotosEquipos.append(fotoM)
                   
                elif prestamos.tabla  == "Teclados":
                    datosTeclado = Teclados.objects.filter(id_teclado = equipo)
                    for datoT in datosTeclado:
                        conexionT = datoT.conexion
                        marcaT = datoT.marca
                        modeloT = datoT.modelo
                        fotoT = datoT.foto

                        if conexionT == "I":

                       
                            teclado = "Inalámbrico" + " " + marcaT + " " + modeloT
                        elif conexionT == "A":
                            teclado = "Alámbrico" + " " + marcaT + " " + modeloT
                       
                        
                    equipoPrestadoClasificacion.append("Teclado " + teclado)
                    fotosEquipos.append(fotoT)
                    
                elif prestamos.tabla  == "Mouses":
                    datosMouse = Mouses.objects.filter(id_mouse = equipo)
                    for datoR in datosMouse:
                        conexionR = datoR.conexion
                        marcaR = datoR.marca
                        modeloR = datoR.modelo
                        fotoR = datoR.foto

                        if conexionR == "I":

                       
                            raton = "Inalámbrico" + " " + marcaR + " " + modeloR
                        elif conexionR == "A":
                            raton = "Alámbrico" + " " + marcaR + " " + modeloR

                    equipoPrestadoClasificacion.append("Mouse " + raton)
                    fotosEquipos.append(fotoR)
                   
                elif prestamos.tabla  == "Telefonos":
                    datosTelefono = Telefonos.objects.filter(id_telefono = equipo)
                    for datoTel in datosTelefono:
                        conexionTel = datoTel.conexion
                        marcaTel = datoTel.marca
                        modeloTel = datoTel.modelo
                        fotoTel = datoTel.foto
                        if conexionTel == "I":

                            telefono = "Inalámbrico" + " " + marcaTel + " " + modeloTel
                            
                        elif conexionTel == "A":
                            telefono = "Alámbrico" + " " + marcaTel + " " + modeloTel
                       
                        
                    equipoPrestadoClasificacion.append("Teléfono " + telefono)
                    fotosEquipos.append(fotoTel)
                    
                elif prestamos.tabla  == "MemoriasUSB":
                    datosMemoria = MemoriasUSB.objects.filter(id_usb = equipo)
                    for datoUSB in datosMemoria:
                        
                        marcaUsb = datoUSB.marca
                        modeloUsb = datoUSB.modelo
                        capacidadUsb = datoUSB.capacidad
                        fotoUsb = "Sin foto"
                       
                        usb = marcaUsb + " " + modeloUsb + " " + capacidadUsb
                    equipoPrestadoClasificacion.append("Memoria USB " + usb)
                    fotosEquipos.append(fotoUsb)
                   
            



            
            
        
            #areasEnActivos = ["1"]
            
        for id in empleadosNoAplica:
          
                
            if id != None:
                datosEmpleado = Empleados.objects.filter(id_empleado = id) #["1", "Sistemas", "rojo"]
                
                if datosEmpleado:
                    for dato in datosEmpleado:
                        nombreEmpleado = dato.nombre
                        apellidosEmpleado = dato.apellidos
                        areaEmpleado = dato.id_area_id
                        datosArea = Areas.objects.filter(id_area=areaEmpleado)
                        
                        if datosArea:
                            for dato in datosArea:
                                nombreArea = dato.nombre
                                color = dato.color
            
                datosCompletosEmpleadosNoAplica.append([nombreEmpleado, apellidosEmpleado, nombreArea, color])
            
        lista = zip(prestamosNOaplicaDev, datosCompletosEmpleadosNoAplica,  equipoPrestadoClasificacion, fotosEquipos)

        #prestamos que aun no se devuelven
        
        empleadosQuenoHanDevuelto = []
        datosCompletosEmpleadosQueAunNoHanDevuelto = []
        equipoAunNoHanDevueltoClasificacion = []
        fotosEquiposAunNoHanDevuelto = []

        for prestaAunNoHanDevuelto in prestamosSINdevolver:
                
            empleadosQuenoHanDevuelto.append(prestaAunNoHanDevuelto.id_empleado_id)

            if prestaAunNoHanDevuelto.tabla == "otro":
                
                equipoAunNoHanDevueltoClasificacion.append(prestaAunNoHanDevuelto.otro)
            
            elif prestaAunNoHanDevuelto.tabla != "otro":
                equipo1 = prestaAunNoHanDevuelto.id_producto

                if prestaAunNoHanDevuelto.tabla == "Impresoras":
                    
                    datosImpresora1= Impresoras.objects.filter(id_impresora = equipo1)
                    for dato1 in datosImpresora1:
                        marcaI1 = dato1.marca
                        modeloI1 = dato1.modelo
                        fotoI1 = dato1.imagen
                        impresora1 = marcaI1 + " " + modeloI1
                    equipoAunNoHanDevueltoClasificacion.append("Impresora " + impresora1)
                    fotosEquiposAunNoHanDevuelto.append(fotoI1)
                
                elif prestaAunNoHanDevuelto.tabla  == "Equipos":
                    datosEquipo1= Equipos.objects.filter(id_equipo = equipo1)
                    for datos1 in datosEquipo1:
                        tipoE1 = datos1.tipo
                        marcaE1 = datos1.marca
                        modeloE1 = datos1.modelo
                        fotoE1 = datos1.imagen
                        equipoC1 = tipoE1 + " " + marcaE1 + " " + modeloE1
                    equipoAunNoHanDevueltoClasificacion.append("Equipo " + equipoC1)
                    fotosEquiposAunNoHanDevuelto.append(fotoE1)
                    
                elif prestaAunNoHanDevuelto.tabla  == "DiscosDuros":
                    datosDiscos1= DiscosDuros.objects.filter(id_disco = equipo1)
                    for datoD1 in datosDiscos1:
                        tipoD1 = datoD1.tipo
                        marcaD1 = datoD1.marca
                        fotoD1 = "Sin foto"
                       
                        disco1 = tipoD1 + " " + marcaD1
                    equipoAunNoHanDevueltoClasificacion.append("Disco Duro " + disco1)
                    fotosEquiposAunNoHanDevuelto.append(fotoD1)
                  
                elif prestaAunNoHanDevuelto.tabla  == "Monitores":
                    datosMonitor1= Monitores.objects.filter(id_monitor = equipo1)
                    for datoM1 in datosMonitor1:
                        marcaM1 = datoM1.marca
                        modeloM1= datoM1.modelo
                        fotoM1 = datoM1.foto
                       
                        monitor1 = marcaM1 + " " + modeloM1
                    equipoAunNoHanDevueltoClasificacion.append("Monitor " + monitor1)
                    fotosEquiposAunNoHanDevuelto.append(fotoM1)
                   
                elif prestaAunNoHanDevuelto.tabla  == "Teclados":
                    datosTeclado1 = Teclados.objects.filter(id_teclado = equipo1)
                    for datoT1 in datosTeclado1:
                        conexionT1 = datoT1.conexion
                        marcaT1 = datoT1.marca
                        modeloT1 = datoT1.modelo
                        fotoT1 = datoT1.foto

                        if conexionT1 == "I":

                       
                            teclado1 = "Inalámbrico" + " " + marcaT1 + " " + modeloT1
                        elif conexionT1 == "A":
                            teclado1 = "Alámbrico" + " " + marcaT1 + " " + modeloT1
                       
                        
                    equipoAunNoHanDevueltoClasificacion.append("Teclado " + teclado1)
                    fotosEquiposAunNoHanDevuelto.append(fotoT1)
                    
                elif prestaAunNoHanDevuelto.tabla  == "Mouses":
                    datosMouse1 = Mouses.objects.filter(id_mouse = equipo1)
                    for datoR1 in datosMouse1:
                        conexionR1 = datoR1.conexion
                        marcaR1 = datoR1.marca
                        modeloR1 = datoR1.modelo
                        fotoR1 = datoR1.foto

                        if conexionR1 == "I":

                       
                            raton1 = "Inalámbrico" + " " + marcaR1 + " " + modeloR1
                        elif conexionR1 == "A":
                            raton1 = "Alámbrico" + " " + marcaR1 + " " + modeloR1

                    equipoAunNoHanDevueltoClasificacion.append("Mouse " + raton1)
                    fotosEquiposAunNoHanDevuelto.append(fotoR1)
                   
                elif prestaAunNoHanDevuelto.tabla  == "Telefonos":
                    datosTelefono1 = Telefonos.objects.filter(id_telefono = equipo1)
                    for datoTel1 in datosTelefono1:
                        conexionTel1 = datoTel1.conexion
                        marcaTel1 = datoTel1.marca
                        modeloTel1 = datoTel1.modelo
                        fotoTel1 = datoTel1.foto
                        if conexionTel1 == "I":

                            telefono1 = "Inalámbrico" + " " + marcaTel1 + " " + modeloTel1
                            
                        elif conexionTel1 == "A":
                            telefono1 = "Alámbrico" + " " + marcaTel1 + " " + modeloTel1
                       
                        
                    equipoAunNoHanDevueltoClasificacion.append("Teléfono " + telefono1)
                    fotosEquiposAunNoHanDevuelto.append(fotoTel1)
                    
                elif prestaAunNoHanDevuelto.tabla  == "MemoriasUSB":
                    datosMemoria1 = MemoriasUSB.objects.filter(id_usb = equipo1)
                    for datoUSB1 in datosMemoria1:
                        
                        marcaUsb1 = datoUSB1.marca
                        modeloUsb1 = datoUSB1.modelo
                        capacidadUsb1 = datoUSB1.capacidad
                        fotoUsb1 = "Sin foto"
                       
                        usb1 = marcaUsb1 + " " + modeloUsb1 + " " + capacidadUsb1
                    equipoAunNoHanDevueltoClasificacion.append("Memoria USB " + usb1)
                    fotosEquiposAunNoHanDevuelto.append(fotoUsb1)
    
        
   
            
        
           
            
        for ids1 in empleadosQuenoHanDevuelto:
          
                
            if ids1 != None:
                datosEmpleados1 = Empleados.objects.filter(id_empleado = ids1) #["1", "Sistemas", "rojo"]
                
                if datosEmpleados1:
                    for datos in datosEmpleados1:
                        nombreEmpleados1 = datos.nombre
                        apellidosEmpleados1 = datos.apellidos
                        areaEmpleados1 = datos.id_area_id
                        datosAreas1 = Areas.objects.filter(id_area=areaEmpleados1)
                        
                        if datosAreas1:
                            for datos in datosAreas1:
                                nombreAreas1 = datos.nombre
                                colors1 = datos.color
            
                datosCompletosEmpleadosQueAunNoHanDevuelto.append([nombreEmpleados1, apellidosEmpleados1, nombreAreas1, colors1])
            
        lista2 = zip(prestamosSINdevolver, datosCompletosEmpleadosQueAunNoHanDevuelto,  equipoAunNoHanDevueltoClasificacion, fotosEquiposAunNoHanDevuelto)
        listaModal = zip(prestamosSINdevolver, datosCompletosEmpleadosQueAunNoHanDevuelto,  equipoAunNoHanDevueltoClasificacion, fotosEquiposAunNoHanDevuelto)

        #prestamos ya devueltos
        
        empleadosQueDevolvieron = []
        datosCompletosEmpleadosQueDevolvieron = []
        equipoDevueltoClasificacion = []
        fotosEquipoDevuelto = []

        for prestaDevuelto in prestamosSIdevolvueltos:
                
            empleadosQueDevolvieron.append(prestaDevuelto.id_empleado_id)

            if prestaDevuelto.tabla == "otro":
                
                equipoDevueltoClasificacion.append(prestaDevuelto.otro)
            
            elif prestaDevuelto.tabla != "otro":
                equipo2 = prestaDevuelto.id_producto

                if prestaDevuelto.tabla == "Impresoras":
                    
                    datosImpresora2= Impresoras.objects.filter(id_impresora = equipo2)
                    for dato2 in datosImpresora2:
                        marcaI2 = dato2.marca
                        modeloI2 = dato2.modelo
                        fotoI2 = dato2.imagen
                        impresora2 = marcaI2 + " " + modeloI2
                    equipoDevueltoClasificacion.append("Impresora " + impresora2)
                    fotosEquipoDevuelto.append(fotoI2)
                
                elif prestaDevuelto.tabla  == "Equipos":
                    datosEquipo2= Equipos.objects.filter(id_equipo = equipo2)
                    for datos2 in datosEquipo2:
                        tipoE2 = datos2.tipo
                        marcaE2 = datos2.marca
                        modeloE2 = datos2.modelo
                        fotoE2 = datos2.imagen
                        equipoC2 = tipoE2 + " " + marcaE2 + " " + modeloE2
                    equipoDevueltoClasificacion.append("Equipo " + equipoC2)
                    fotosEquipoDevuelto.append(fotoE2)
                    
                elif prestaDevuelto.tabla  == "DiscosDuros":
                    datosDiscos2= DiscosDuros.objects.filter(id_disco = equipo2)
                    for datoD2 in datosDiscos2:
                        tipoD2 = datoD2.tipo
                        marcaD2 = datoD2.marca
                        fotoD2 = "Sin foto"
                       
                        disco2 = tipoD2 + " " + marcaD2
                    equipoDevueltoClasificacion.append("Disco Duro " + disco2)
                    fotosEquipoDevuelto.append(fotoD2)
                  
                elif prestaDevuelto.tabla  == "Monitores":
                    datosMonitor2= Monitores.objects.filter(id_monitor = equipo2)
                    for datoM2 in datosMonitor2:
                        marcaM2 = datoM2.marca
                        modeloM2= datoM2.modelo
                        fotoM2 = datoM2.foto
                       
                        monitor2 = marcaM2 + " " + modeloM2
                    equipoDevueltoClasificacion.append("Monitor " + monitor2)
                    fotosEquipoDevuelto.append(fotoM2)
                   
                elif prestaDevuelto.tabla  == "Teclados":
                    datosTeclado2 = Teclados.objects.filter(id_teclado = equipo2)
                    for datoT2 in datosTeclado2:
                        conexionT2 = datoT2.conexion
                        marcaT2 = datoT2.marca
                        modeloT2 = datoT2.modelo
                        fotoT2 = datoT2.foto

                        if conexionT2 == "I":

                       
                            teclado2 = "Inalámbrico" + " " + marcaT2 + " " + modeloT2
                        elif conexionT2 == "A":
                            teclado2 = "Alámbrico" + " " + marcaT2 + " " + modeloT2
                       
                        
                    equipoDevueltoClasificacion.append("Teclado " + teclado2)
                    fotosEquipoDevuelto.append(fotoT2)
                    
                elif prestaDevuelto.tabla  == "Mouses":
                    datosMouse2 = Mouses.objects.filter(id_mouse = equipo2)
                    for datoR2 in datosMouse2:
                        conexionR2 = datoR2.conexion
                        marcaR2 = datoR2.marca
                        modeloR2 = datoR2.modelo
                        fotoR2 = datoR2.foto

                        if conexionR2 == "I":

                       
                            raton2 = "Inalámbrico" + " " + marcaR2 + " " + modeloR2
                        elif conexionR1 == "A":
                            raton2 = "Alámbrico" + " " + marcaR2 + " " + modeloR2

                    equipoDevueltoClasificacion.append("Mouse " + raton2)
                    fotosEquipoDevuelto.append(fotoR2)
                   
                elif prestaDevuelto.tabla  == "Telefonos":
                    datosTelefono2 = Telefonos.objects.filter(id_telefono = equipo2)
                    for datoTel2 in datosTelefono2:
                        conexionTel2 = datoTel2.conexion
                        marcaTel2 = datoTel2.marca
                        modeloTel2 = datoTel2.modelo
                        fotoTel2 = datoTel2.foto
                        if conexionTel2 == "I":

                            telefono2 = "Inalámbrico" + " " + marcaTel2 + " " + modeloTel2
                            
                        elif conexionTel2 == "A":
                            telefono2 = "Alámbrico" + " " + marcaTel2 + " " + modeloTel2
                       
                        
                    equipoDevueltoClasificacion.append("Teléfono " + telefono2)
                    fotosEquipoDevuelto.append(fotoTel2)
                    
                elif prestaDevuelto.tabla  == "MemoriasUSB":
                    datosMemoria2 = MemoriasUSB.objects.filter(id_usb = equipo2)
                    for datoUSB2 in datosMemoria2:
                        
                        marcaUsb2 = datoUSB2.marca
                        modeloUsb2 = datoUSB2.modelo
                        capacidadUsb2 = datoUSB2.capacidad
                        fotoUsb2 = "Sin foto"
                       
                        usb2 = marcaUsb2 + " " + modeloUsb2 + " " + capacidadUsb2
                    equipoDevueltoClasificacion.append("Memoria USB " + usb2)
                    fotosEquipoDevuelto.append(fotoUsb2)
    
    
        
        
            
        
            #areasEnActivos = ["1"]
            
        for Idd in empleadosQueDevolvieron:
          
                
            if Idd != None:
                datoEmpleados2 = Empleados.objects.filter(id_empleado = Idd) #["1", "Sistemas", "rojo"]
                
                if datoEmpleados2:
                    for dat2 in datoEmpleados2:
                        nomEmpleados2 = dat2.nombre
                        apellEmpleados2 = dat2.apellidos
                        areaEmplea2 = dat2.id_area_id
                        datAreas2 = Areas.objects.filter(id_area=areaEmplea2)
                        
                        if datAreas2:
                            for da2 in datAreas2:
                                nomAreas2 = da2.nombre
                                col2 = da2.color
            
                datosCompletosEmpleadosQueDevolvieron.append([nomEmpleados2, apellEmpleados2, nomAreas2, col2])
            
        lista3 = zip(prestamosSIdevolvueltos, datosCompletosEmpleadosQueDevolvieron, equipoDevueltoClasificacion, fotosEquipoDevuelto )
        fechaHoy = datetime.now()

        if "prestamoFinalizado" in request.session:
            prestamoFinalizado=True
            textoActualizado= request.session['prestamoFinalizado']
            del request.session["prestamoFinalizado"]

            return render(request, "prestamos/verPrestamo.html", {"estaEnVerPrestamos": estaEnVerPrestamos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "prestamosSINdevolver":prestamosSINdevolver, 
                                                           "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "prestamosNOaplicaDev":prestamosNOaplicaDev, "numeroNoti":numeroNoti,  "prestamosSIdevolvueltos":prestamosSIdevolvueltos, "lista2":lista2,"lista3":lista3, "foto":foto,
                                                            "equipoPrestadoClasificacion":equipoPrestadoClasificacion,"fechaHoy":fechaHoy, "datosCompletosEmpleadosQueAunNoHanDevuelto": datosCompletosEmpleadosQueAunNoHanDevuelto, "listaModal":listaModal, "prestamoFinalizado":prestamoFinalizado, "textoActualizado":textoActualizado})
            
           
       
        
        
        
        

        return render(request, "prestamos/verPrestamo.html", {"estaEnVerPrestamos": estaEnVerPrestamos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "lista":lista, "prestamosSINdevolver":prestamosSINdevolver, 
                                                           "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "prestamosNOaplicaDev":prestamosNOaplicaDev, "numeroNoti":numeroNoti,  "prestamosSIdevolvueltos":prestamosSIdevolvueltos, "lista2":lista2,"lista3":lista3, "foto":foto,
                                                            "equipoPrestadoClasificacion":equipoPrestadoClasificacion,"fechaHoy":fechaHoy, "datosCompletosEmpleadosQueAunNoHanDevuelto": datosCompletosEmpleadosQueAunNoHanDevuelto, "listaModal":listaModal})

    else:
        return redirect('/login/') #redirecciona a url de inicio

def firmarPrestamoDevolucion(request):

    if "idSesion" in request.session:

        estaEnVerPrestamos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        nombreCompleto = nombre + " " + apellidos
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)

        if request.method == "POST":

            idPrestamo = request.POST['idPrestamoAFirmar']

            infoPrestamo = PrestamosSistemas.objects.filter(id_prestamo = idPrestamo)
            
            
            nombreDepartamento = ""
            colorDepartamento = ""
            nombreCompletoEmpleado = ""
            nombreEquipo = ""
            imagenEquipo = ""

            for dato in infoPrestamo:
                tabla = dato.tabla
                idequipoPrestamo = dato.id_producto

                if tabla == "otro":
                    nombreEquipo = dato.otro
                    imagenEquipo = False
                elif tabla == "Impresoras":
                    consultaImpresoras = Impresoras.objects.filter(id_impresora = idequipoPrestamo)
                    for datoPres in consultaImpresoras:
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        imagen = datoPres.imagen
                    nombreEquipo = "Impresora "+marca + " " + modelo
                    imagenEquipo = imagen
                elif tabla == "Equipos":
                    consultaEquipos = Equipos.objects.filter(id_equipo = idequipoPrestamo)
                    for datoPres in consultaEquipos:
                        tipo = datoPres.tipo
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        imagen = datoPres.imagen
                    nombreEquipo = "Computadora "+tipo+" "+marca + " " + modelo
                    imagenEquipo = imagen
                elif tabla == "DiscosDuros":
                    consultaDiscos = DiscosDuros.objects.filter(id_disco = idequipoPrestamo)
                    for datoPres in consultaDiscos:
                        tipo = datoPres.tipo
                        marca = datoPres.marca
                        dimension = datoPres.dimension
                        imagen = False
                    nombreEquipo = "Disco Duro "+tipo + " " + marca + " " + dimension
                    imagenEquipo = imagen
                elif tabla == "Monitores":
                    consultaMonitores = Monitores.objects.filter(id_monitor = idequipoPrestamo)
                    for datoPres in consultaMonitores:
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        imagen = datoPres.foto
                    nombreEquipo = "Monitor "+marca + " " + modelo
                    imagenEquipo = imagen
                elif tabla == "Teclados":
                    consultaTeclados = Teclados.objects.filter(id_teclado = idequipoPrestamo)
                    for datoPres in consultaTeclados:
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        if datoPres.conexion == "A":
                            conexion = "Alámbrico"
                        elif datoPres.conexion == "I":
                            conexion = "Inalámbrico"
                        imagen = datoPres.foto
                    nombreEquipo = "Teclado "+conexion+" "+marca + " " + modelo
                    imagenEquipo = imagen
                elif tabla == "Mouses":
                    consultaMouses = Mouses.objects.filter(id_mouse = idequipoPrestamo)
                    for datoPres in consultaMouses:
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        if datoPres.conexion == "A":
                            conexion = "Alámbrico"
                        elif datoPres.conexion == "I":
                            conexion = "Inalámbrico"
                        imagen = datoPres.foto
                    nombreEquipo = "Mouse "+conexion+" "+marca + " " + modelo
                    imagenEquipo = imagen
                elif tabla == "Teléfonos":
                    consultaTelefonos = Telefonos.objects.filter(id_telefono = idequipoPrestamo)
                    for datoPres in consultaTelefonos:
                        marca = datoPres.marca
                        modelo = datoPres.modelo
                        if datoPres.conexion == "A":
                            conexion = "Alámbrico"
                        elif datoPres.conexion == "I":
                            conexion = "Inalámbrico"
                        imagen = datoPres.foto
                    nombreEquipo = "Teléfono "+conexion+" "+marca + " " + modelo
                    imagenEquipo = imagen
                

                
                
                
                
                #info empleado
                idEmpleado = dato.id_empleado_id
                infoEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for dato in infoEmpleado:
                    nombre = dato.nombre
                    apellidos = dato.apellidos

                    idArea = dato.id_area_id
                nombreCompletoEmpleado = nombre + " " + apellidos
                datosArea = Areas.objects.filter(id_area=idArea)

                for dato in datosArea:
                    nombreDepartamento = dato.nombre
                    colorDepartamento = dato.color


            return render(request, "prestamos/firmaAgregarPrestamo.html", {"estaEnVerPrestamos": estaEnVerPrestamos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo,
                                                           "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti,  "numeroNoti":numeroNoti,   "foto":foto, "infoPrestamo":infoPrestamo,
                                            "nombreDepartamento":nombreDepartamento,
                                            "colorDepartamento":colorDepartamento,
                                            "nombreCompletoEmpleado":nombreCompletoEmpleado,
                                            "nombreEquipo":nombreEquipo,
                                            "imagen":imagen})

            
    else:
        return redirect("/login/")



def actualizarPrestamos(request):

    if "idSesion" in request.session:

        if request.method == "POST":

            idPrestamo = request.POST['idPrestamoGuardarFirma']

            condiciones = request.POST['condiciones']

            canvasLargo1 = request.POST['canvasData']
            format1, imgstr1 = canvasLargo1.split(';base64,')
            ext1 = format1.split('/')[-1]
            archivo1 = ContentFile(base64.b64decode(imgstr1), name= "imagen" + '.' + ext1)
            fecha_Hoy = date.today()

            actualizrPrestamo = PrestamosSistemas.objects.get(id_prestamo=idPrestamo)
            actualizrPrestamo.fecha_entrega = fecha_Hoy
            actualizrPrestamo.firma_devolucion = archivo1
            actualizrPrestamo.save()

            actualizar = PrestamosSistemas.objects.filter(id_prestamo=idPrestamo).update( estatus = "Finalizado", condiciones = condiciones)
                
            if actualizar:
                
                textoPrestamo = "Se ha entregado el material del préstamo  "+ str(idPrestamo) + " con éxito!"
                            
                request.session['prestamoFinalizado'] = textoPrestamo
                
                return redirect('/verPrestamos/')
    else:
        return redirect("/login/")





  
        
        
        
    

    
def agregarEncuestas(request):
        
    if "idSesion" in request.session:
    
        estaEnAgregarEncuestas= True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #----si se da clic en el boton en guardar encuesta
        if request.method == "POST":
            
            nombreEncuesta = request.POST['nombreEnc']
            cantidadMultiples = request.POST['multiples']
            cantidadAbiertas = request.POST['abiertas']
            fechaHoy =datetime.now()
            pregunta = "pregunta"
            clasificacion = "clasificacion"
            multiple = 0
            preguntasMultiples=[]
            clasificacionesMultiples = []
            
            for respuestaMultiple in range(int(cantidadMultiples)):
                multiple= multiple + 1
                nameMultiple = pregunta + str(multiple)
                nameClasificacion = clasificacion + str(multiple)
                textoPreguntaMultiple = request.POST[nameMultiple]
                textoClasificacion = request.POST[nameClasificacion]
                preguntasMultiples.append(textoPreguntaMultiple)
                clasificacionesMultiples.append(textoClasificacion)

            listaMultiples = zip (preguntasMultiples, clasificacionesMultiples)
            
            preguntaAb = "preguntaAb"
            abierta = 0
            preguntasAbiertas = []
            
            for respuestaAbierta in range(int(cantidadAbiertas)):
                abierta = abierta + 1
                nameAbierta = preguntaAb + str(abierta)
                textoPreguntaAbierta = request.POST[nameAbierta]
                preguntasAbiertas.append(textoPreguntaAbierta)
                
            
            
            
            #--registro de encuesta
            registrarEncuesta = Encuestas(fecha_encuesta=fechaHoy, nombre_encuesta = nombreEncuesta, preguntas_multiples =cantidadMultiples, preguntas_abiertas =cantidadAbiertas)
            registrarEncuesta.save()
         
            if registrarEncuesta:
                registrarEncuesta = Encuestas.objects.count()
                
              
                    
                for preguntaMultiple, clasificacion in listaMultiples:
                    
                    registroPreguntaMultiple = Preguntas(id_encuesta = Encuestas.objects.get(id_encuesta=registrarEncuesta), pregunta = preguntaMultiple, tipo = "M", clasificacion = clasificacion)
                    
                    registroPreguntaMultiple.save()
                    
                for preguntaAbierta in preguntasAbiertas:
                        
                    registroPreguntaAbierta = Preguntas(id_encuesta = Encuestas.objects.get(id_encuesta=registrarEncuesta),  pregunta = preguntaAbierta, clasificacion = "A", tipo = "A")
                    
                    registroPreguntaAbierta.save()
                
            encuestaGuardada = True
            encuestaGuardadaTexto = "La encuesta fue guardada con éxito!"
            return render(request, "Encuestas/agregarEncuestas.html", {"estaEnAgregarEncuestas":estaEnAgregarEncuestas,"id_admin":id_admin, "encuestaGuardada": encuestaGuardada, "encuestaGuardadaTexto": encuestaGuardadaTexto, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
                    
            

        return render(request, "Encuestas/agregarEncuestas.html", {"estaEnAgregarEncuestas":estaEnAgregarEncuestas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect ('/login/')

def verEncuestas(request):
    
    if "idSesion" in request.session:
        
        estaEnVerEncuestas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        inforEncuestas = Encuestas.objects.all()
        
        

        return render(request, "Encuestas/verEncuestas.html", {"estaEnVerEncuestas":estaEnVerEncuestas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "inforEncuestas":inforEncuestas , "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
    
        return redirect ('/login/')

def preguntas(request):
    
    if "idSesion" in request.session:
        
        estaEnVerEncuestas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        if request.method == "POST":
            
            id_encuesta = request.POST['id_encuesta']
            
            infoEncuesta = Encuestas.objects.filter(id_encuesta=id_encuesta)

            preguntasEncuesta = Preguntas.objects.filter(id_encuesta_id__id_encuesta=id_encuesta)

            preguntasMultiples=[]
            preguntasAbiertas =[]

            for pregunta in preguntasEncuesta:
                if pregunta.tipo == "M":
                    preguntasMultiples.append([pregunta.id_pregunta, pregunta.pregunta, pregunta.clasificacion])
                elif pregunta.tipo == "A":
                    preguntasAbiertas.append([pregunta.id_pregunta, pregunta.pregunta])



        
        

            return render(request, "Encuestas/preguntas.html", {"estaEnVerEncuestas":estaEnVerEncuestas, "preguntasMultiples" : preguntasMultiples, "preguntasAbiertas" : preguntasAbiertas,"infoEncuesta":infoEncuesta, "id_encuesta": id_encuesta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
    
        return redirect ('/login/')

    
def reporteMousesActivos(request):
    
    if "idSesion" in request.session:
    
        if request.method == "POST":

            estado= request.POST['activo'] #Recibe activo o inactivo
            
            
        
        mouses = Mouses.objects.filter(activo__icontains = estado) #Todos los mouses activos
        
        numero_mouses = 0
        for mouse in mouses:
            numero_mouses +=1 #Contador de mouses totales
            
        if numero_mouses == 0:
            numero_mouses =1
        
        division = numero_mouses // 9 #Resultado entero, sin residuo... 9 por hoja
        residuo = numero_mouses%9 #residuo hay 2
        
        
        
        if residuo == 0:
            #hojas iguales a division.
            hojasIguales = True
            
        if residuo != 0:
            division = division + 1   #Número de hojas total. 2
            
        #QUITAR ESTO PARA OTRA HOJA
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Mouses Activos'+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        #HASTA AQUI
            
        contadorMouses = 0
        contadorHojas = 1
        #For que se repite por cada hoja
        for hoja2 in range(division):
            
            #HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
            datosMouses= Mouses.objects.filter(activo__icontains=estado) ##1 equipo
            
            
            ids =[]
            conexiones = []
            marcas = []
            modelos = []
            estados = []
            urls_imagenes = []
            equiposPropietarios = []
            empleadosPropietarios = []
            base_dir = str(settings.BASE_DIR)
            
            if contadorHojas == 5:
                contadorMouses = 0
                contadorMousesXHoja = 0
                for datoM in datosMouses:
                    
                    contadorMouses += 1 #10
                    if contadorMouses > 36 and contadorMouses <=45:
                        imagen = datoM.foto
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idequipo = datoM.id_equipo_id
                        if idequipo == None:
                            equiposPropietarios.append("Sin equipo asignado")
                            empleadosPropietarios.append("Sin empleado asignado")
                        else:
                            info_equipo = Equipos.objects.filter(id_equipo = idequipo)
                            
                            for dato in info_equipo:
                                tipo = dato.tipo
                                marca = dato.marca
                                modelo = dato.modelo
                                empleado = dato.id_empleado_id
                                nombre_completo = tipo + " " + marca + " " + modelo
                                equiposPropietarios.append(nombre_completo)

                            
                        ids.append(str(datoM.id_mouse))
                        if datoM.conexion == "A":
                            conexiones.append("Alámbrico")
                        elif datoM.conexion == "I":
                            conexiones.append("Inalámbrico")
                        marcas.append(datoM.marca)
                        modelos.append(datoM.modelo)
                        if datoM.estado == "activoFuncional":
                            estados.append("Activo Funcional")
                        elif datoM.estado == "stockUsado":
                            estados.append("Stock Usado")
                        elif datoM.estado == "stockNuevo":
                            estados.append("Stock Nuevo")
                        
                        
                        contadorMousesXHoja +=1
                        
                    
                #solo 9 empleados
                listaMouses = zip(ids, conexiones, marcas, modelos,  estados,urls_imagenes, equiposPropietarios)
                
                contadorHojas = 6
                if contadorMousesXHoja == 9:
                    high = 600 - ((contadorMousesXHoja+1) * 33)
                else:
                    high = 600 - (contadorMousesXHoja * 33)
            
            if contadorHojas == 4:
                contadorMouses = 0
                contadorMousesXHoja = 0
                for datoM in datosMouses:
                    
                    contadorMouses += 1 #10
                    if contadorMouses > 27 and contadorMouses <=36:
                        imagen = datoM.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idequipo = datoM.id_equipo_id
                        if idequipo == None:
                            equiposPropietarios.append("Sin equipo asignado")
                        else:
                            info_equipo = Equipos.objects.filter(id_equipo = idequipo)
                            
                            for dato in info_equipo:
                                tipo = dato.tipo
                                marca = dato.marca
                                modelo = dato.modelo
                                nombre_completo = tipo + " " + marca + " " + modelo
                                equiposPropietarios.append(nombre_completo)
                            
                        ids.append(str(datoM.id_mouse))
                        if datoM.conexion == "A":
                            conexiones.append("Alámbrico")
                        elif datoM.conexion == "I":
                            conexiones.append("Inalámbrico")
                        marcas.append(datoM.marca)
                        modelos.append(datoM.modelo)
                        if datoM.estado == "activoFuncional":
                            estados.append("Activo Funcional")
                        elif datoM.estado == "stockUsado":
                            estados.append("Stock Usado")
                        elif datoM.estado == "stockNuevo":
                            estados.append("Stock Nuevo")
                        
                        
                        contadorMousesXHoja +=1
                        
                    
                #solo 9 empleados
                listaMouses = zip(ids, conexiones, marcas, modelos,  estados,urls_imagenes, equiposPropietarios)
                
                contadorHojas = 5
                if contadorMousesXHoja == 9:
                    high = 600 - ((contadorMousesXHoja+1) * 33)
                else:
                    high = 600 - (contadorMousesXHoja * 33)
                    
                    
            
            if contadorHojas == 3:
                contadorMouses = 0
                contadorMousesXHoja = 0
                for datoM in datosMouses:
                    
                    contadorMouses += 1 #10
                    if contadorMouses > 18 and contadorMouses <=27:
                        imagen = datoM.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idequipo = datoM.id_equipo_id
                        if idequipo == None:
                            equiposPropietarios.append("Sin equipo asignado")
                        else:
                            info_equipo = Equipos.objects.filter(id_equipo = idequipo)
                            
                            for dato in info_equipo:
                                tipo = dato.tipo
                                marca = dato.marca
                                modelo = dato.modelo
                                nombre_completo = tipo + " " + marca + " " + modelo
                                equiposPropietarios.append(nombre_completo)
                            
                        ids.append(str(datoM.id_mouse))
                        if datoM.conexion == "A":
                            conexiones.append("Alámbrico")
                        elif datoM.conexion == "I":
                            conexiones.append("Inalámbrico")
                        marcas.append(datoM.marca)
                        modelos.append(datoM.modelo)
                        if datoM.estado == "activoFuncional":
                            estados.append("Activo Funcional")
                        elif datoM.estado == "stockUsado":
                            estados.append("Stock Usado")
                        elif datoM.estado == "stockNuevo":
                            estados.append("Stock Nuevo")
                        
                        
                        contadorMousesXHoja +=1
                        
                    
                #solo 9 empleados
                listaMouses = zip(ids, conexiones, marcas, modelos, estados, urls_imagenes,equiposPropietarios)
                
                contadorHojas = 4
                if contadorMousesXHoja == 9:
                    high = 600 - ((contadorMousesXHoja+1) * 33)
                else:
                    high = 600 - (contadorMousesXHoja * 33)
                    
                    
            
            if contadorHojas == 2:
                contadorMouses = 0
                contadorMousesXHoja = 0
                for datoM in datosMouses:
                    
                    contadorMouses += 1 #10
                    if contadorMouses > 9 and contadorMouses <=18:
                        imagen = datoM.imagen
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=40, height=40)
                        urls_imagenes.append(img)
                        
                        idequipo = datoM.id_equipo_id
                        if idequipo == None:
                            equiposPropietarios.append("Sin equipo asignado")
                        else:
                            info_equipo = Equipos.objects.filter(id_equipo = idequipo)
                            
                            for dato in info_equipo:
                                tipo = dato.tipo
                                marca = dato.marca
                                modelo = dato.modelo
                                nombre_completo = tipo + " " + marca + " " + modelo
                                equiposPropietarios.append(nombre_completo)
                            
                        ids.append(str(datoM.id_mouse))
                        if datoM.conexion == "A":
                            conexiones.append("Alámbrico")
                        elif datoM.conexion == "I":
                            conexiones.append("Inalámbrico")
                        marcas.append(datoM.marca)
                        modelos.append(datoM.modelo)
                        if datoM.estado == "activoFuncional":
                            estados.append("Activo Funcional")
                        elif datoM.estado == "stockUsado":
                            estados.append("Stock Usado")
                        elif datoM.estado == "stockNuevo":
                            estados.append("Stock Nuevo")
                        
                        
                        contadorMousesXHoja +=1
                        
                    
                #solo 9 empleados
                listaMouses = zip(ids, conexiones, marcas, modelos, estados,urls_imagenes, equiposPropietarios)
                
                contadorHojas = 3
                if contadorMousesXHoja == 9:
                    high = 600 - ((contadorMousesXHoja+1) * 33)
                else:
                    high = 600 - (contadorMousesXHoja * 33)
                    
                        
            if contadorHojas == 1:
                contadorMousesXHoja = 0
                for datoM in datosMouses:
                    
                    contadorMouses += 1 #10
                    if contadorMouses <= 9:
                        imagen = datoM.foto
                        urlimagen = base_dir + '/media/' + str(imagen)
                        img = Image(urlimagen,width=50, height=50)
                        urls_imagenes.append(img)
                        
                        idequipo = datoM.id_equipo_id
                        if idequipo == None:
                            equiposPropietarios.append(["Sin equipo asignado","Sin empleado asignado"] )
                           
                        else:
                            info_equipo = Equipos.objects.filter(id_equipo = idequipo)
                            
                            for dato in info_equipo:
                                tipo = dato.tipo
                                marca = dato.marca
                                modelo = dato.modelo
                                empleadoId = dato.id_empleado_id
                                nombre_completo = tipo + " " + marca + " " + modelo
                                

                                datosEmpleados = Empleados.objects.filter(id_empleado = empleadoId)
                                for e in datosEmpleados:
                                    nombre = e.nombre
                                    apellido = e.apellidos 
                                nombreCompletoEmpleado = nombre + " " + apellido
                          
                                equiposPropietarios.append([nombre_completo,nombreCompletoEmpleado])
                            
                        ids.append(str(datoM.id_mouse))
                        if datoM.conexion == "A":
                            conexiones.append("Alámbrico")
                        elif datoM.conexion == "I":
                            conexiones.append("Inalámbrico")
                        marcas.append(datoM.marca)
                        modelos.append(datoM.modelo)
                        if datoM.estado == "activoFuncional":
                            estados.append("Activo Funcional")
                        elif datoM.estado == "stockUsado":
                            estados.append("Stock Usado")
                        elif datoM.estado == "stockNuevo":
                            estados.append("Stock Nuevo")
                        
                        contadorMousesXHoja +=1
                        
                    
                #solo 9 empleados
                listaMouses = zip(ids, conexiones, marcas, modelos, estados,urls_imagenes, equiposPropietarios)
                
                contadorHojas = 2
                if contadorMousesXHoja == 9:
                    high = 615 - ((contadorMousesXHoja+1) * 33)
                else:
                    high = 615 - (contadorMousesXHoja * 33)
                

            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
            
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            
            c.setFont('Helvetica-Bold', 12)
            if estado == "A":
                c.drawString(390,750, "REPORTE MOUSES ACTIVOS")
            elif estado == "I":
                c.drawString(380,750, "REPORTE MOUSES INACTIVOS")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
            
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
            
            if estado == "A":
                c.drawString(180,660, 'Reporte Mouses Activos')
            elif estado == "I":
                c.drawString(180,660, 'Reporte Mouses Inactivos')
            
            #header de tabla
            styles = getSampleStyleSheet()
            styleBH =styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 9
            
            
            id_mouse = Paragraph('''ID''', styleBH)
            conexion = Paragraph('''Conexión''', styleBH)
            marca = Paragraph('''Marca''', styleBH)
            modelo = Paragraph('''Modelo''', styleBH)
            estado = Paragraph('''Estado''', styleBH)
            foto = Paragraph('''Imagen.''', styleBH)
            
            
            propEquipo = Paragraph('''Equipo al que pertenece''', styleBH)
            filasTabla=[]
            filasTabla.append([id_mouse, conexion, marca, modelo,estado,foto,propEquipo])
            #Tabla
            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7
            
                
            cont = 0
            for idm, conexionm, marcam, modelom, estadom, fotom, propEquipom  in listaMouses:
                campo_mouse = Paragraph(idm, styleN)
                campo_conexion = Paragraph(conexionm, styleN)
                campo_marca = Paragraph(marcam, styleN)
                campo_modelo = Paragraph(modelom, styleN)
               
                campo_estado = Paragraph(estadom, styleN)
                campo_propEquipo = Paragraph(propEquipom[0]  + '''<br/> <br/> '''+ propEquipom[1], styleN)
                
                fila = [campo_mouse, campo_conexion, campo_marca, campo_modelo,campo_estado, fotom, campo_propEquipo]
                filasTabla.append(fila)
                
                high= high - 18 
                
                
            #escribir tabla
            width, height = letter
            tabla = Table(filasTabla, colWidths=[.9 * cm, 2.5 * cm, 2 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 5 * cm
                                               ])
            tabla.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))
            
            for fila in filasTabla:
                tabla.setStyle(([
                ('BACKGROUND', (0, 0), (10,0), colors.crimson),
                ('TEXTCOLOR',(0,0), (1, 1), colors.whitesmoke)
            ]))
            
            tabla.wrapOn(c, width, height)
            tabla.drawOn(c, 50, high)
            
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
    
            #guardar pdf
            c.save()
            #obtener valores de bytesIO y esribirlos en la respuesta
            pdf = buffer.getvalue()
            buffer.close()
            respuesta.write(pdf)
            return respuesta
        
    else:
        return redirect('/login/') #redirecciona a url de inicio

    
def xlMouses(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    if activoa == "A":
        response['Content-Disposition'] = 'attachment; filename=Reporte Mouses-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    else:
        response['Content-Disposition'] = 'attachment; filename=Reporte Mouses Inactivos-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Conexión', 'Marca', 'Modelo', 'Estado', 'Equipo asignado','Empleado asignado']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    propietariosEquipo = []
    propietarioEmpleado = []
    estados = []
    
    
    infoMouses = Mouses.objects.filter(activo = activoa)
        
    for mouse in infoMouses:
        id_equipo = mouse.id_equipo_id
     
        
        if id_equipo == None:
            nombreEquipo = "Sin equipo asignado"
            propietarioEm = "Sin propieatrio"
            
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
          
        
      
            
        else:
            datosEquipo = Equipos.objects.filter(id_equipo = id_equipo)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEquipo:
                tipo = dato.tipo
                marca = dato.marca
                modelo = dato.modelo
                id_emple = dato.id_empleado_id
                
                infoEmple = Empleados.objects.filter(id_empleado = id_emple)
                for dato in infoEmple:
                    nombre = dato.nombre
                    apellido = dato.apellidos
            nombreEquipo = tipo + " " + marca + " " + modelo
            propietarioEm = nombre + " " + apellido
           
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
        
        
           
        
    conexiones = []
    estados = []
    
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    mouses = Mouses.objects.filter(activo = activoa)
    
    datosMouses = []
    cont=0
    for x in mouses:
        cont+=1

        if x.conexion == "A":
            conexiones.append("Alámbrico")
        elif x.conexion == "I":
            conexiones.append("Inalámbrico")

        if x.estado == "activoFuncional":
            estados.append("Activo Funcional")
        elif x.estado == "stockUsado":
            estados.append("Stock Usado")
        elif x.estado == "stockNuevo":
            estados.append("Stock Nuevo")
        elif x.estado == "basura":
            estados.append("Basura")


        datosMouses.append([x.id_mouse, conexiones[cont-1], x.marca, x.modelo, estados[cont-1], propietariosEquipo[cont-1], propietarioEmpleado[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for mousito in datosMouses:
        numero_fila+=1
        for columna in range(len(mousito)):
            hoja.write(numero_fila, columna, str(mousito[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 

def xlTeclados(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    if activoa == "A":
        response['Content-Disposition'] = 'attachment; filename=Reporte Teclados-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    else:
        response['Content-Disposition'] = 'attachment; filename=Reporte Teclados Inactivos-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'  
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Conexión', 'Marca', 'Modelo', 'Estado', 'Equipo asignado','Empleado asignado']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    propietariosEquipo = []
    propietarioEmpleado = []
    estados = []
    
    
    infoTeclados = Teclados.objects.filter(activo = activoa)
        
    for teclado in infoTeclados:
        id_equipo = teclado.id_equipo_id
     
        
        if id_equipo == None:
            nombreEquipo = "Sin equipo asignado"
            propietarioEm = "Sin propieatrio"
            
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
          
        
      
            
        else:
            datosEquipo = Equipos.objects.filter(id_equipo = id_equipo)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEquipo:
                tipo = dato.tipo
                marca = dato.marca
                modelo = dato.modelo
                id_emple = dato.id_empleado_id
                
                infoEmple = Empleados.objects.filter(id_empleado = id_emple)
                for dato in infoEmple:
                    nombre = dato.nombre
                    apellido = dato.apellidos
            nombreEquipo = tipo + " " + marca + " " + modelo
            propietarioEm = nombre + " " + apellido
           
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
        
        
           
        
    conexiones = []
    estados = []
    
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    teclados = Teclados.objects.filter(activo = activoa)
    
    datosTeclados = []
    cont=0
    for x in teclados:
        cont+=1

        if x.conexion == "A":
            conexiones.append("Alámbrico")
        elif x.conexion == "I":
            conexiones.append("Inalámbrico")

        if x.estado == "activoFuncional":
            estados.append("Activo Funcional")
        elif x.estado == "stockUsado":
            estados.append("Stock Usado")
        elif x.estado == "stockNuevo":
            estados.append("Stock Nuevo")
        elif x.estado == "basura":
            estados.append("Basura")


        datosTeclados.append([x.id_teclado, conexiones[cont-1], x.marca, x.modelo, estados[cont-1], propietariosEquipo[cont-1], propietarioEmpleado[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for tecladito in datosTeclados:
        numero_fila+=1
        for columna in range(len(tecladito)):
            hoja.write(numero_fila, columna, str(tecladito[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 


def xlMonitores(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    if activoa == "A":
        response['Content-Disposition'] = 'attachment; filename=Reporte Monitores-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    else:
        response['Content-Disposition'] = 'attachment; filename=Reporte Monitores Inactivos-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id', 'Marca', 'Modelo', 'Estado', 'Equipo asignado','Empleado asignado']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    propietariosEquipo = []
    propietarioEmpleado = []
    estados = []
    
    
    infoMonitores = Monitores.objects.filter(activo = activoa)
        
    for monitor in infoMonitores:
        id_equipo = monitor.id_equipo_id
     
        
        if id_equipo == None:
            nombreEquipo = "Sin equipo asignado"
            propietarioEm = "Sin propieatrio"
            
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
          
        
      
            
        else:
            datosEquipo = Equipos.objects.filter(id_equipo = id_equipo)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEquipo:
                tipo = dato.tipo
                marca = dato.marca
                modelo = dato.modelo
                id_emple = dato.id_empleado_id
                
                infoEmple = Empleados.objects.filter(id_empleado = id_emple)
                for dato in infoEmple:
                    nombre = dato.nombre
                    apellido = dato.apellidos
            nombreEquipo = tipo + " " + marca + " " + modelo
            propietarioEm = nombre + " " + apellido
           
            
            propietariosEquipo.append(nombreEquipo)
            propietarioEmpleado.append(propietarioEm)
        
        
           
        
  
    estados = []
    
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    monitores = Monitores.objects.filter(activo = activoa)
    
    datosMonitores = []
    cont=0
    for x in monitores:
        cont+=1

       

        if x.estado == "activoFuncional":
            estados.append("Activo Funcional")
        elif x.estado == "stockUsado":
            estados.append("Stock Usado")
        elif x.estado == "stockNuevo":
            estados.append("Stock Nuevo")
        elif x.estado == "basura":
            estados.append("Basura")


        datosMonitores.append([x.id_monitor, x.marca, x.modelo, estados[cont-1], propietariosEquipo[cont-1], propietarioEmpleado[cont-1]])
            
        
    estilo_fuente = xlwt.XFStyle()
    for monitorsito in datosMonitores:
        numero_fila+=1
        for columna in range(len(monitorsito)):
            hoja.write(numero_fila, columna, str(monitorsito[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 


def xlTelefonos(request):
    if request.method == "POST":
    
        activoa= request.POST['activo'] #A o I
            
    response = HttpResponse(content_type='application/ms-excel')
    if activoa == "A":
        response['Content-Disposition'] = 'attachment; filename=Reporte Teléfonos-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    else:
        response['Content-Disposition'] = 'attachment; filename=Reporte Teléfonos Inactivos-'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Equipos')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id','Encargado', 'Departamento', 'Tipo de conexión', 'Marca','Modelo','Estado','Nodo', 'Extensión']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    departamentos = []
    encargados = []
    estados = []
    
    
    infoTelefonos = Telefonos.objects.filter(activo = activoa)
        
    for telefono in infoTelefonos:
        id_empleado = telefono.id_empleado_id
     
        
        if id_empleado == None:
            empleado = "Sin encargado asignado"
            area = "Sin departamento"
            
            encargados.append(empleado)
            departamentos.append(area)
           
          
        
      
            
        else:
            datosEncargado = Empleados.objects.filter(id_empleado = id_empleado)#filtro de los empleados que esten dentro de un area especifica
            
            for dato in datosEncargado:
                nombreEncargado = dato.nombre
                apellidosEncargado = dato.apellidos
                depa = dato.id_area_id
                
                
                infoDepa = Areas.objects.filter(id_area = depa)
                for dato in infoDepa:
                    nombreA = dato.nombre
                 
            empleado = nombreEncargado + " " + apellidosEncargado 
            area = nombreA 
           
            
            encargados.append(empleado)
            departamentos.append(area)
        
        
           
        
    conexiones = []
    estados = []
    
    #lista la lista de propietarios de equipos, incluyendo los que no tienen propietario.
        
    telefonos = Telefonos.objects.filter(activo = activoa)
    
    datosTelefonos = []
    cont=0
    for x in telefonos:
        cont+=1

       
        if x.conexion == "A":
            conexiones.append("Alámbrico")
        elif x.conexion == "I":
            conexiones.append("Inalámbrico")

        if x.estado == "activoFuncional":
            estados.append("Activo Funcional")
        elif x.estado == "stockUsado":
            estados.append("Stock Usado")
        elif x.estado == "stockNuevo":
            estados.append("Stock Nuevo")
        elif x.estado == "basura":
            estados.append("Basura")


        datosTelefonos.append([x.id_telefono,encargados[cont-1], departamentos[cont-1],conexiones[cont-1], x.marca, x.modelo, estados[cont-1],x.nodo,x.extension])
            
        
    estilo_fuente = xlwt.XFStyle()
    for telefonsito in datosTelefonos:
        numero_fila+=1
        for columna in range(len(telefonsito)):
            hoja.write(numero_fila, columna, str(telefonsito[columna]), estilo_fuente)
    
    libro.save(response)
    return response    
    #creación 

def verSoportes(request):
    if "idSesion" in request.session:
        
        estaEnVerSoportes = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        consultaSoportes = SoportesTecnicos.objects.all()
        solicitantes = []
        nombresEquipos = []
        tipos = []
        resuelto_internos = []
        proveedores = []

        for soporte in consultaSoportes:
            #empleado
            idEmpleadoSolicitante = soporte.id_empleado_id
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
            for dato in consultaEmpleado:
                nombre = dato.nombre
                apellidos = dato.apellidos

            nombreCompleto = nombre + " " + apellidos

            solicitantes.append(nombreCompleto)

            #Nombre equipo
            idEquipoAtendido = soporte.equipo_soporte
            tabla = soporte.tabla

            if tabla == "Equipos":
                consultaEquipo = Equipos.objects.filter(id_equipo = int(idEquipoAtendido))
                for dato in consultaEquipo:
                    tipoEquipo = dato.tipo
                    marcaEquipo = dato.marca
                    modeloEquipo = dato.modelo

                equipoEntero = tipoEquipo + " " + marcaEquipo + " " + modeloEquipo
                nombresEquipos.append(equipoEntero)
                tipos.append("Equipo de computo")

            elif tabla == "Impresoras":
                consultaImpresora = Impresoras.objects.filter(id_impresora = int(idEquipoAtendido))
                for datoImpresora in consultaImpresora:
                    marcaImpresora = datoImpresora.marca
                    modeloImpresora = datoImpresora.modelo

                impresoraEntera = marcaImpresora + " " + modeloImpresora
                nombresEquipos.append(impresoraEntera)
                tipos.append("Impresoras")

            elif tabla == "Otros":
                nombresEquipos.append("No aplica")
                tipos.append("Otros")

            
            resueltoInterno = soporte.resuelto_interno
            if resueltoInterno == "S":
                resuelto_internos.append("Si")
                proveedores.append("No aplica")
            elif resueltoInterno == None:
                resuelto_internos.append("No")
                proveedor = soporte.proveedor
                proveedores.append(proveedor)


        lista = zip(consultaSoportes, solicitantes, nombresEquipos, tipos, resuelto_internos, proveedores)



        return render(request,"SoportesTecnicos/verSoportes.html", {"estaEnVerSoportes": estaEnVerSoportes, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "lista":lista, "proveedores":proveedores})
    else:
        return redirect('/login/')

def agregarSoporteEquipoComputo(request):
    if "idSesion" in request.session:
        
        soportes = True
        estaEnSoporteEquipos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Lista de equipos para select
        infoEquipos = Equipos.objects.filter(activo = "A")
     
        
        empleadosEquipo= []
        for empleado in infoEquipos:
            idEmpleado = empleado.id_empleado_id
            
            if idEmpleado == None:
                texto = "Sin propietario"
                empleadosEquipo.append([texto])

            else:
                empleados = Empleados.objects.filter(id_empleado = idEmpleado)

                for empleadoEquipo in empleados:
                    nombre = empleadoEquipo.nombre
                    apellidos = empleadoEquipo.apellidos
                    empleadosEquipo.append([nombre,apellidos])
            
        lista = zip(infoEquipos, empleadosEquipo)

        #Si se le dio clic al botón
        if request.method == "POST":
            equipoProp= request.POST['equipoProp']
            tabla = request.POST['tabla']
            operaciones = request.POST.getlist('operacion')
            observaciones = request.POST['descripcion']
            proveedor = request.POST['proveedor']

            fecha = datetime.now()

            consultaEquipo = Equipos.objects.filter(id_equipo = equipoProp)
            for dato in consultaEquipo:
                idEmpleado = dato.id_empleado_id

            
            
            todasOperaciones = ""
            for operacion in operaciones:
                todasOperaciones += operacion + " - "

            if proveedor == "":
                resueltoInterno = "S"
                registroSoporte = SoportesTecnicos(id_empleado = Empleados.objects.get(id_empleado = idEmpleado), fecha_soporte = fecha, 
            equipo_soporte = equipoProp, tabla = "Equipos", operacion = todasOperaciones,
            observaciones = observaciones, resuelto_interno = resueltoInterno, resuelto_proveedor="No aplica")
            else:
                resueltoInterno = "N"
                registroSoporte = SoportesTecnicos(id_empleado = Empleados.objects.get(id_empleado = idEmpleado), fecha_soporte = fecha, 
            equipo_soporte = equipoProp, tabla = "Equipos", operacion = todasOperaciones,
            observaciones = observaciones, resuelto_interno = resueltoInterno, resuelto_proveedor = proveedor)

            registroSoporte.save()

            if registroSoporte:
                soporteGuardado = True

                return render(request,"SoportesTecnicos/agregarSoporteEquipoComputo.html", {"Soportes": soportes,"estaEnSoporteEquipos":estaEnSoporteEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "lista":lista, "soporteGuardado":soporteGuardado})
            

    

        return render(request,"SoportesTecnicos/agregarSoporteEquipoComputo.html", {"Soportes": soportes,"estaEnSoporteEquipos":estaEnSoporteEquipos, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "lista":lista})
    else:
        return redirect('/login/')

def agregarSoporteImpresora(request):
    if "idSesion" in request.session:
        
        soportes = True
        estaEnSoporteImpresora = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        infoImpresoras = Impresoras.objects.filter(activo = "A")

        areasImpresora= []
        for impresora in infoImpresoras:
            idArea = impresora.id_area_id
            infoArea = Areas.objects.filter(id_area = idArea)

            for dato in infoArea:
                nombreArea = dato.nombre
                areasImpresora.append(nombreArea)
            
        lista = zip(infoImpresoras, areasImpresora)

        listaEmpleados = Empleados.objects.filter(activo="A")
        
        
        #Si se le dio clic al botón
        if request.method == "POST":
            equipo= request.POST['equipoProp']
            tabla = request.POST['tabla']
            operaciones = request.POST.getlist('operacion')
            observaciones = request.POST['descripcion']
            solicitante = request.POST['solicitante']

            fecha = datetime.now()

            consultaImpresora = Impresoras.objects.filter(id_impresora = equipo)
            

            
            
            todasOperaciones = ""
            for operacion in operaciones:
                todasOperaciones += operacion + " - "

            
            registroSoporte = SoportesTecnicos(id_empleado = Empleados.objects.get(id_empleado = solicitante), fecha_soporte = fecha, 
            equipo_soporte = equipo, tabla = "Impresoras", operacion = todasOperaciones,
            observaciones = observaciones, resuelto_interno = "S", resuelto_proveedor = "No aplica")
           

            registroSoporte.save()

            if registroSoporte:
                soporteGuardado = True

                return render(request,"SoportesTecnicos/agregarSoporteImpresora.html", {"Soportes": soportes,"estaEnSoporteImpresora":estaEnSoporteImpresora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "lista":lista, "soporteGuardado":soporteGuardado})
            


        return render(request,"SoportesTecnicos/agregarSoporteImpresora.html", {"Soportes": soportes,"estaEnSoporteImpresoras": estaEnSoporteImpresora, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "lista":lista, "listaEmpleados":listaEmpleados})
    else:
        return redirect('/login/')

def agregarSoporteOtros(request):
    if "idSesion" in request.session:
        
        soportes = True
        estaEnSoporteOtro = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()

        listaEmpleados = Empleados.objects.filter(activo="A")

        #Si se le dio clic al botón
        if request.method == "POST":
            empleadoSolicitante= request.POST['idEmpeladoSolicitante']
           
            operacion = request.POST[('operacion')]
            observaciones = request.POST['observaciones']

            fecha = datetime.now()

            registroSoporte = SoportesTecnicos(id_empleado = Empleados.objects.get(id_empleado = empleadoSolicitante), fecha_soporte = fecha, 
            tabla = "Otros", operacion = operacion,
            observaciones = observaciones, resuelto_interno = "S")
            
            registroSoporte.save()

            if registroSoporte:
                soporteGuardado = True

                return render(request,"SoportesTecnicos/agregarSoporteOtros.html", {"Soportes": soportes,"estaEnSoporteOtros": estaEnSoporteOtro, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "listaEmpleados":listaEmpleados, "soporteGuardado":soporteGuardado})
            


        return render(request,"SoportesTecnicos/agregarSoporteOtros.html", {"Soportes": soportes,"estaEnSoporteOtros": estaEnSoporteOtro, "id_admin":id_admin,"nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,
        "listaEmpleados":listaEmpleados})
    else:
        return redirect('/login/')
    
    
def verImplementaciones(request):
    
    if "idSesion" in request.session:

        implementaciones = True
        estaEnVerImplementaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        listaImplementaciones = ImplementacionSoluciones.objects.all()
        

        return render(request, "Implementaciones/verImplementaciones.html", {"estaEnVerImplementaciones":estaEnVerImplementaciones,"implementaciones":implementaciones,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti
                                                       , "foto":foto, "listaImplementaciones":listaImplementaciones})
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarImplementacion(request):
    
    if "idSesion" in request.session:

        implementaciones = True
        estaEnAgregarImplementacion = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        foto = fotoAdmin(request)
        
        nombreCompleto = nombre + " " + apellidos
        
        #Si se da clic a un botón
        if request.method == "POST":
            tituloProblema = request.POST['tituloProblema']
            fechaComienzo = request.POST['fechaComienzo']
            fcomienzo_separada = fechaComienzo.split("/") #29   06    2018            2018     29   06
            fcomienzo_normal = fcomienzo_separada[2] + "-" + fcomienzo_separada[0] + "-" + fcomienzo_separada[1]

            fechaFinal = request.POST['fechaFinal']
            ffinal_separada = fechaComienzo.split("/") #29   06    2018            2018     29   06
            ffinal_normal = ffinal_separada[2] + "-" + ffinal_separada[0] + "-" + ffinal_separada[1]

            descripcion = request.POST['descripcion']

            nameInput = "solucion"
            
            if request.POST.get(nameInput, False): #Checkeado
                solucionado = "N"
            elif request.POST.get(nameInput, True): #No checkeado
                solucionado = "S"

            registroImplementacion = ImplementacionSoluciones(titulo_problema = tituloProblema, descripcion = descripcion,
            fecha_comienzo = fcomienzo_normal, fecha_terminada = ffinal_normal, resuelto = solucionado, revisado = "N")
            registroImplementacion.save()

            if registroImplementacion:
                implementacionGuardada = True
                    
                #Mandar correo a Edgar para revisión y firma
                
                # Obtener el último id de la implementación.

                strUltimaImplementacion = ImplementacionSoluciones.objects.count()
                ultimaImplementacion = str(strUltimaImplementacion)

                # Mandar correo
                correo = "auxiliar.sistemas@customco.com.mx"
                asunto = "CS | Solicitud de revision de Implementación de Solución"
                plantilla = "Implementaciones/correoimp.html"
                html_mensaje = render_to_string(plantilla, {"tituloProblema": tituloProblema, "ultimaImplementacion": ultimaImplementacion, "descripcion":descripcion})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = [correo]
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                

                return render(request,"Implementaciones/agregarImplementacion.html", {"estaEnAgregarImplementacion": estaEnAgregarImplementacion,"implementaciones":implementaciones, "id_admin":id_admin,
                                                           "nombreCompleto":nombreCompleto, "correo":correo, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "implementacionGuardada":implementacionGuardada})
            
        

        return render(request,"Implementaciones/agregarImplementacion.html", {"estaEnAgregarImplementacion": estaEnAgregarImplementacion,"implementaciones":implementaciones, "id_admin":id_admin,
                                                           "nombreCompleto":nombreCompleto, "correo":correo, 
                                                          "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto})
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
def verMochilas(request):
    
    if "idSesion" in request.session:

        estaEnVerMochilas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #Listas a utilizar
        mochilasActivas = []
        mochilasActivasPrestamos = []
        mochilasActivasPrestamos = []
        idsMochilasPrestamos = []
        
        #Lista de todos los mouses
        listaMochilas = Mochilas.objects.all()
        mochilasPrestadas = PrestamosSistemas.objects.filter(devolucion = "N", tabla = "Mochilas")
        for moP in mochilasPrestadas:
            idMochila = moP.id_producto
            idsMochilasPrestamos.append(idMochila)

        
        for mochila in listaMochilas:
            idMochila = str(mochila.id_mochila)
            marca = mochila.marca
            modelo = mochila.modelo
            estado = mochila.estado
            fotoMochila = mochila.foto
            if mochila.id_empleado_id == None:
                ConEmpleado = False

            else:
                ConEmpleado = True
                idEmpleado = str(mochila.id_empleado_id)
            activo = mochila.activo
            
            if activo == "A":
                if ConEmpleado == True:
                     
                    #sacar info de eempleado
                    infoEmpleado = Empleados.objects.filter(id_empleado = int(idEmpleado))
                    for dato in infoEmpleado:
                        idArea = dato.id_area_id
                        nombre = dato.nombre
                        apellidos = dato.apellidos
                        
                        empleado = nombre + " " + apellidos
                        
                        consultaArea = Areas.objects.filter(id_area = idArea)
                        for datoArea in consultaArea:
                            nombreArea = datoArea.nombre
                            colorArea = datoArea.color
                    
                   

                elif ConEmpleado == False:
                    empleado = "Sin empleado"
                    nombreArea = "Sin departamento"
                    colorArea = "Sin color"
                        
                mochilasActivas.append([idMochila, marca, modelo, estado, fotoMochila, empleado, nombreArea, colorArea])

                if idMochila in idsMochilasPrestamos:
                    for mochilaP in mochilasPrestadas:
                        idMochilaP = mochilaP.id_producto
                        if idMochila == idMochilaP:
                            fechaEntrega = mochilaP.fecha_prestamo
                            firmaEn = mochilaP.firma_entrega
                        
                        mochilasActivasPrestamos.append([fechaEntrega, firmaEn])
                else:
                    mochilasActivasPrestamos.append("Sin prestamo")
                
            lista = zip(mochilasActivas, mochilasActivasPrestamos)

                
                            





            #No tiene un equipo asignado, puede variar el estado..
            
            if activo == "I":
                mochilasActivasPrestamos.append([idMochila, marca, modelo, estado, fotoMochila])

            
            if "idMonitorBaja" in request.session:
                baja = True
                mensaje = "Se dio de baja al monitor " + request.session['idMonitorBaja']
                del request.session["idMonitorBaja"]
                return render(request, "Sistemas/Mochilas/verMochilas.html", {"estaEnVerMochilas":estaEnVerMochilas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mochilasActivas":mochilasActivas, "mochilasActivasPrestamos":mochilasActivasPrestamos,
            "mochilasActivasPrestamos":mochilasActivasPrestamos, "lista":lista, "idsMochilasPrestamos":idsMochilasPrestamos, "baja":baja, "mensaje":mensaje})

            if "idMonitorBaja" in request.session:
                alta = True
                mensaje = "Se dio de alta al monitor " + request.session['idMonitorBaja']
                del request.session["idMonitorBaja"]
                return render(request, "Sistemas/Mochilas/verMochilas.html", {"estaEnVerMochilas":estaEnVerMochilas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto,"mochilasActivas":mochilasActivas, "mochilasActivasPrestamos":mochilasActivasPrestamos,
            "mochilasActivasPrestamos":mochilasActivasPrestamos, "lista":lista, "idsMochilasPrestamos":idsMochilasPrestamos, "alta":alta, "mensaje":mensaje})

        return render(request, "Sistemas/Mochilas/verMochilas.html", {"estaEnVerMochilas":estaEnVerMochilas,"id_admin":id_admin, "lista":lista, "mochilasActivasPrestamos":mochilasActivasPrestamos, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, "mochilasActivas":mochilasActivas, "mochilasActivasPrestamos":mochilasActivasPrestamos})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def agregarMochila(request):
    
    if "idSesion" in request.session:

        estaEnAgregarMochilas = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        
        
        cartuchosNoti = notificacionInsumos()
        mantenimientosNoti = notificacionLimpiezas()
        numeroNoti = numNoti()
        
        #consulta equipos
        empleados = Empleados.objects.filter(activo="A")
        
        #Si se le dio clic al botón de Guardar Monitor
        if request.method == "POST":
            
            marcaMochila = request.POST['marcaMochila']
            modeloMochila = request.POST['modeloMochila']
            estadoMochila = request.POST['estadoMochila']
            imagenchila = request.FILES.get('imagenMochila')
            empleadoMochila = request.POST['empleadoMochila']
            
            #Si el mouse fue guardado sin equipo..
            if empleadoMochila == "SinEmpleado":
                registroMochila = Mochilas(marca = marcaMochila, modelo = modeloMochila, 
                                       estado = estadoMochila, foto = imagenchila, activo = "I")
                registroMochila.save()
            
            #Si el mouse se guardó con un equipo...
            elif empleadoMochila != "SinEquipo":
                intEmpleado = int(empleadoMochila)
                registroMochila = Mochilas(marca = marcaMochila, modelo = modeloMochila, 
                                       estado = estadoMochila, foto = imagenchila, activo = "A", id_empleado = Empleados.objects.get(id_empleado = empleadoMochila))
                registroMochila.save()
            
            #Variables para el mensaje
            if registroMochila:
                registroMochilaCompletado = True
                texto  = "Se ha registrado la mochila "+ marcaMochila + " " + modeloMochila
                
            return render(request, "Sistemas/Mochilas/agregarMochilas.html", {"estaEnAgregarMochilas":estaEnAgregarMochilas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, 
                                                                            "empleados":empleados, "registroMochilaCompletado":registroMochilaCompletado, "texto":texto})

        

        return render(request, "Sistemas/Mochilas/agregarMochilas.html", {"estaEnAgregarMochilas":estaEnAgregarMochilas,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "correo":correo, "cartuchosNoti":cartuchosNoti, "mantenimientosNoti": mantenimientosNoti, "numeroNoti":numeroNoti, "foto":foto, 
                                                                            "empleados":empleados})
    else:
        return redirect('/login/') #redirecciona a url de inicio